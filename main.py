from fastapi import FastAPI, HTTPException, Depends, Header, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import httpx
import os
from dotenv import load_dotenv

from session_manager import SessionManager
from scam_detector import ScamDetector
from reply_generator import ReplyGenerator
from intelligence_extractor import IntelligenceExtractor

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Agentic Scam Honeypot API",
    description="Backend REST API for detecting and engaging with scam messages",
    version="1.0.0"
)

# Global session manager
session_manager = SessionManager()

# Configuration
API_KEY = os.getenv("API_KEY", "default-api-key")
CALLBACK_URL = os.getenv("CALLBACK_URL")


# Pydantic models
class MessageRequest(BaseModel):
    """Request model for incoming scam messages."""
    session_id: str = Field(..., description="Unique identifier for the conversation session")
    message: str = Field(..., description="The scam message content")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Optional metadata about the message")


class MessageResponse(BaseModel):
    """Response model for message processing."""
    session_id: str
    reply: str
    is_scam: bool
    confidence: float
    intelligence: Dict[str, list]
    session_ended: bool


class CallbackPayload(BaseModel):
    """Payload sent to callback URL when session ends."""
    session_id: str
    message_count: int
    intelligence: Dict[str, list]
    messages: list
    is_scam_confirmed: bool
    created_at: str
    last_activity: str


# Authentication dependency
async def verify_api_key(x_api_key: str = Header(...)):
    """Verify API key from request header."""
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return x_api_key


# Helper function to send callback
async def send_callback(session_data: Dict[str, Any]):
    """Send callback to configured URL with session data."""
    if not CALLBACK_URL:
        print("No callback URL configured, skipping callback")
        return
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                CALLBACK_URL,
                json=session_data,
                timeout=10.0
            )
            response.raise_for_status()
            print(f"Callback sent successfully for session {session_data['session_id']}")
    except Exception as e:
        print(f"Failed to send callback: {str(e)}")


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Agentic Scam Honeypot API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "active_sessions": len(session_manager.get_active_sessions())
    }


@app.post("/api/message", response_model=MessageResponse)
async def process_message(
    request: MessageRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    Process incoming scam message and generate reply.
    
    This endpoint:
    1. Accepts a message with session_id
    2. Detects if it's a scam using rule-based logic
    3. Extracts intelligence (UPI IDs, phone numbers, URLs)
    4. Generates a human-like reply to engage the scammer
    5. Manages session state
    6. Sends a callback when the conversation ends
    """
    # Get or create session
    session = session_manager.get_or_create_session(request.session_id)
    
    # Add scammer message to session
    session.add_message("scammer", request.message)
    
    # Detect scam intent
    scam_detection = ScamDetector.detect_scam(request.message)
    
    # Update session scam confirmation
    if scam_detection["is_scam"] and scam_detection["confidence"] > 0.5:
        session.is_scam_confirmed = True
    
    # Generate reply
    message_count = session.get_message_count()
    reply = ReplyGenerator.generate_reply(message_count, request.message)
    
    # Add bot reply to session
    session.add_message("bot", reply)
    
    # Check if conversation should end
    should_end = ReplyGenerator.should_end_conversation(message_count)
    
    if should_end:
        session.end_session()
        # Schedule callback in background
        background_tasks.add_task(send_callback, session.to_dict())
    
    # Return response
    return MessageResponse(
        session_id=session.session_id,
        reply=reply,
        is_scam=scam_detection["is_scam"],
        confidence=scam_detection["confidence"],
        intelligence=session.intelligence,
        session_ended=not session.is_active
    )


@app.get("/api/session/{session_id}")
async def get_session(
    session_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get session details."""
    session = session_manager.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session.to_dict()


@app.delete("/api/session/{session_id}")
async def end_session(
    session_id: str,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """Manually end a session and trigger callback."""
    session = session_manager.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.is_active:
        session.end_session()
        # Schedule callback in background
        background_tasks.add_task(send_callback, session.to_dict())
    
    return {
        "message": "Session ended",
        "session_id": session_id
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    uvicorn.run(app, host=host, port=port)
