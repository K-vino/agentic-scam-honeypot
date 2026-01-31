import httpx
import logging
from typing import Optional
from datetime import datetime
from app.models.schemas import SessionSummary, CallbackRequest
from app.core.config import settings
from app.services.session_manager import Session

logger = logging.getLogger(__name__)


class CallbackService:
    """Handle callbacks when engagement completes"""
    
    async def send_callback(self, session: Session) -> bool:
        """
        Send a callback with session summary
        
        Returns:
            True if callback was sent successfully, False otherwise
        """
        if not settings.callback_url:
            logger.info(f"No callback URL configured. Session {session.session_id} completed.")
            return False
        
        try:
            # Build session summary
            summary = SessionSummary(
                sessionId=session.session_id,
                messageCount=session.message_count,
                scamIntents=session.scam_intents,
                confidence=session.get_average_confidence(),
                intelligence=session.intelligence,
                conversationHistory=session.conversation_history,
                engagementDuration=session.get_duration(),
                completedAt=datetime.utcnow(),
                terminationReason=session.termination_reason or "completed"
            )
            
            # Build callback request
            callback_data = CallbackRequest(
                sessionId=session.session_id,
                summary=summary,
                status="completed"
            )
            
            # Send async HTTP POST request
            async with httpx.AsyncClient(timeout=settings.callback_timeout) as client:
                response = await client.post(
                    settings.callback_url,
                    json=callback_data.model_dump(),
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    logger.info(f"Callback sent successfully for session {session.session_id}")
                    return True
                else:
                    logger.error(
                        f"Callback failed for session {session.session_id}. "
                        f"Status: {response.status_code}, Response: {response.text}"
                    )
                    return False
                    
        except httpx.TimeoutException:
            logger.error(f"Callback timeout for session {session.session_id}")
            return False
        except Exception as e:
            logger.error(f"Callback error for session {session.session_id}: {str(e)}")
            return False
    
    def log_summary(self, session: Session):
        """Log session summary to console"""
        logger.info(f"=== Session Summary: {session.session_id} ===")
        logger.info(f"Message Count: {session.message_count}")
        logger.info(f"Scam Intents: {[intent.value for intent in session.scam_intents]}")
        logger.info(f"Confidence: {session.get_average_confidence():.2f}")
        logger.info(f"Duration: {session.get_duration():.2f}s")
        logger.info(f"UPI IDs: {session.intelligence.upiIds}")
        logger.info(f"Phone Numbers: {session.intelligence.phoneNumbers}")
        logger.info(f"URLs: {session.intelligence.urls}")
        logger.info(f"Termination Reason: {session.termination_reason}")


# Global callback service instance
callback_service = CallbackService()
