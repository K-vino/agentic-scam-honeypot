from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class MessageEvent(BaseModel):
    """Incoming scam message event"""
    sessionId: str = Field(..., description="Unique session identifier")
    message: str = Field(..., description="Message content from potential scammer")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ScamIntent(str, Enum):
    """Types of scam intent detected"""
    FINANCIAL_FRAUD = "financial_fraud"
    PHISHING = "phishing"
    UPI_SCAM = "upi_scam"
    FAKE_PRIZE = "fake_prize"
    JOB_SCAM = "job_scam"
    ROMANCE_SCAM = "romance_scam"
    TECH_SUPPORT = "tech_support"
    NONE = "none"


class MessageResponse(BaseModel):
    """Response to a message event"""
    sessionId: str
    reply: str
    scamDetected: bool
    scamIntents: List[ScamIntent]
    confidence: float = Field(ge=0.0, le=1.0)
    shouldContinue: bool
    extractedIntelligence: Dict[str, List[str]] = Field(default_factory=dict)


class IntelligenceReport(BaseModel):
    """Intelligence extracted from scam conversation"""
    upiIds: List[str] = Field(default_factory=list)
    phoneNumbers: List[str] = Field(default_factory=list)
    urls: List[str] = Field(default_factory=list)
    bankDetails: List[str] = Field(default_factory=list)
    emailAddresses: List[str] = Field(default_factory=list)


class SessionSummary(BaseModel):
    """Final callback data when engagement completes"""
    sessionId: str
    messageCount: int
    scamIntents: List[ScamIntent]
    confidence: float
    intelligence: IntelligenceReport
    conversationHistory: List[Dict[str, str]]
    engagementDuration: float  # in seconds
    completedAt: datetime
    terminationReason: str


class CallbackRequest(BaseModel):
    """Callback payload sent when engagement completes"""
    sessionId: str
    summary: SessionSummary
    status: str = "completed"
