from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import MessageEvent, MessageResponse, ScamIntent
from app.core.security import verify_api_key
from app.services.session_manager import session_manager
from app.services.scam_detector import scam_detector
from app.services.intelligence_extractor import intelligence_extractor
from app.services.reply_generator import reply_generator
from app.services.callback_service import callback_service
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["honeypot"])


@router.post("/message", response_model=MessageResponse)
async def process_message(
    event: MessageEvent,
    api_key: str = Depends(verify_api_key)
) -> MessageResponse:
    """
    Process an incoming scam message event
    
    - Detects scam intent using rule-based logic
    - Extracts intelligence (UPI IDs, phone numbers, URLs)
    - Generates human-like reply
    - Manages session state
    - Triggers callback when engagement completes
    """
    
    # Get or create session
    session = session_manager.get_or_create_session(event.sessionId)
    
    # Add incoming message to history
    session.add_message("scammer", event.message)
    
    # Detect scam intent
    is_scam, scam_intents, confidence = scam_detector.detect(event.message)
    
    # Update session with detection results
    for intent in scam_intents:
        session.add_scam_intent(intent)
    session.add_confidence_score(confidence)
    
    # Extract intelligence
    intel_report = intelligence_extractor.extract(event.message)
    
    # Merge with existing intelligence
    session.intelligence.upiIds.extend(intel_report.upiIds)
    session.intelligence.phoneNumbers.extend(intel_report.phoneNumbers)
    session.intelligence.urls.extend(intel_report.urls)
    session.intelligence.bankDetails.extend(intel_report.bankDetails)
    session.intelligence.emailAddresses.extend(intel_report.emailAddresses)
    
    # Deduplicate
    session.intelligence.upiIds = list(set(session.intelligence.upiIds))
    session.intelligence.phoneNumbers = list(set(session.intelligence.phoneNumbers))
    session.intelligence.urls = list(set(session.intelligence.urls))
    session.intelligence.bankDetails = list(set(session.intelligence.bankDetails))
    session.intelligence.emailAddresses = list(set(session.intelligence.emailAddresses))
    
    # Check if session should terminate
    should_terminate, termination_reason = session.should_terminate()
    
    # Generate reply
    if should_terminate:
        reply = reply_generator.generate_goodbye()
        should_continue = False
        session.terminate(termination_reason)
        
        # Send callback
        await callback_service.send_callback(session)
        callback_service.log_summary(session)
        
        # Clean up session
        session_manager.delete_session(event.sessionId)
    else:
        reply = reply_generator.generate_reply(
            event.message,
            session.scam_intents,
            session.message_count - 1  # Exclude current message
        )
        should_continue = True
    
    # Add reply to history
    session.add_message("agent", reply)
    
    # Build response
    response = MessageResponse(
        sessionId=event.sessionId,
        reply=reply,
        scamDetected=is_scam,
        scamIntents=scam_intents if scam_intents else [ScamIntent.NONE],
        confidence=confidence,
        shouldContinue=should_continue,
        extractedIntelligence={
            "upiIds": intel_report.upiIds,
            "phoneNumbers": intel_report.phoneNumbers,
            "urls": intel_report.urls,
            "bankDetails": intel_report.bankDetails,
            "emailAddresses": intel_report.emailAddresses,
        }
    )
    
    return response


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_sessions": session_manager.get_active_session_count()
    }


@router.post("/cleanup")
async def cleanup_sessions(api_key: str = Depends(verify_api_key)):
    """Manually trigger cleanup of expired sessions"""
    session_manager.cleanup_expired_sessions()
    return {
        "status": "success",
        "active_sessions": session_manager.get_active_session_count()
    }
