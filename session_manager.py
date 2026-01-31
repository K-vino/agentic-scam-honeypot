from typing import Dict, List, Optional
from datetime import datetime
from intelligence_extractor import IntelligenceExtractor


class Session:
    """Represents a conversation session."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: List[Dict] = []
        self.intelligence: Dict = {
            "upi_ids": [],
            "phone_numbers": [],
            "urls": []
        }
        self.is_scam_confirmed = False
        self.created_at = datetime.utcnow()
        self.last_activity = datetime.utcnow()
        self.is_active = True
    
    def add_message(self, role: str, content: str):
        """Add a message to the session."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.last_activity = datetime.utcnow()
        
        # Extract intelligence from scammer messages
        if role == "scammer":
            intel = IntelligenceExtractor.extract(content)
            self._merge_intelligence(intel)
    
    def _merge_intelligence(self, new_intel: Dict):
        """Merge new intelligence with existing intelligence."""
        for key in ["upi_ids", "phone_numbers", "urls"]:
            existing = set(self.intelligence[key])
            existing.update(new_intel[key])
            self.intelligence[key] = list(existing)
    
    def get_message_count(self) -> int:
        """Get total number of messages."""
        return len(self.messages)
    
    def get_last_message(self) -> Optional[str]:
        """Get the last message content."""
        if self.messages:
            return self.messages[-1]["content"]
        return None
    
    def end_session(self):
        """Mark session as ended."""
        self.is_active = False
    
    def to_dict(self) -> Dict:
        """Convert session to dictionary for callback."""
        return {
            "session_id": self.session_id,
            "messages": self.messages,
            "intelligence": self.intelligence,
            "is_scam_confirmed": self.is_scam_confirmed,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "message_count": self.get_message_count()
        }


class SessionManager:
    """Manages conversation sessions in memory."""
    
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
    
    def create_session(self, session_id: str) -> Session:
        """Create a new session."""
        if session_id in self.sessions:
            return self.sessions[session_id]
        
        session = Session(session_id)
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get an existing session."""
        return self.sessions.get(session_id)
    
    def get_or_create_session(self, session_id: str) -> Session:
        """Get existing session or create new one."""
        if session_id not in self.sessions:
            return self.create_session(session_id)
        return self.sessions[session_id]
    
    def delete_session(self, session_id: str):
        """Delete a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def get_active_sessions(self) -> List[Session]:
        """Get all active sessions."""
        return [s for s in self.sessions.values() if s.is_active]
