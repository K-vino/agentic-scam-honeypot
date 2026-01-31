import re
from typing import Optional


class ScamDetector:
    """Detects scam intent using rule-based logic."""
    
    # Keywords and patterns that indicate scam messages
    SCAM_KEYWORDS = [
        "urgent", "verify", "account", "suspended", "blocked",
        "lottery", "winner", "prize", "congratulations",
        "click here", "verify now", "update", "confirm",
        "bank", "credit card", "debit card", "otp", "password",
        "refund", "tax", "customs", "delivery",
        "won", "selected", "claim", "expires",
        "pay", "payment", "transfer", "fund",
        "kbc", "kaun banega crorepati"
    ]
    
    SCAM_PATTERNS = [
        r'\b(?:click|tap)\s+(?:here|link|below)\b',
        r'\bverify\s+(?:your|now|immediately)\b',
        r'\baccount\s+(?:suspended|blocked|locked)\b',
        r'\bcongratulations.*won\b',
        r'\bclaim.*prize\b',
        r'\bexpires?\s+(?:today|soon|in)\b',
        r'\bact\s+(?:now|fast|immediately)\b',
        r'\breply\s+(?:yes|no|stop)\b',
    ]
    
    @classmethod
    def detect_scam(cls, message: str) -> dict:
        """
        Detect if a message is a scam.
        
        Returns:
            dict with 'is_scam' boolean and 'confidence' score
        """
        message_lower = message.lower()
        
        # Check for keywords
        keyword_matches = sum(1 for keyword in cls.SCAM_KEYWORDS if keyword in message_lower)
        
        # Check for patterns
        pattern_matches = sum(1 for pattern in cls.SCAM_PATTERNS if re.search(pattern, message_lower))
        
        # Calculate confidence score
        total_matches = keyword_matches + (pattern_matches * 2)  # Weight patterns more
        confidence = min(total_matches / 5.0, 1.0)  # Normalize to 0-1
        
        is_scam = confidence > 0.3  # Threshold for scam detection
        
        return {
            "is_scam": is_scam,
            "confidence": round(confidence, 2),
            "keyword_matches": keyword_matches,
            "pattern_matches": pattern_matches
        }
