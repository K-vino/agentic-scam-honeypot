import re
from typing import List, Dict, Any


class IntelligenceExtractor:
    """Extracts scam intelligence from messages."""
    
    # Regex patterns for extraction
    UPI_PATTERN = re.compile(r'\b[\w\.\-]+@[\w]+\b', re.IGNORECASE)
    PHONE_PATTERN = re.compile(r'\b(?:\+91[\-\s]?)?[6-9]\d{9}\b')
    URL_PATTERN = re.compile(r'https?://[^\s]+|www\.[^\s]+')
    
    @classmethod
    def extract(cls, message: str) -> Dict[str, List[str]]:
        """Extract UPI IDs, phone numbers, and URLs from message."""
        intelligence = {
            "upi_ids": [],
            "phone_numbers": [],
            "urls": []
        }
        
        # Extract UPI IDs
        upi_matches = cls.UPI_PATTERN.findall(message)
        intelligence["upi_ids"] = list(set(upi_matches))
        
        # Extract phone numbers
        phone_matches = cls.PHONE_PATTERN.findall(message)
        intelligence["phone_numbers"] = list(set(phone_matches))
        
        # Extract URLs
        url_matches = cls.URL_PATTERN.findall(message)
        intelligence["urls"] = list(set(url_matches))
        
        return intelligence
    
    @classmethod
    def extract_from_messages(cls, messages: List[str]) -> Dict[str, List[str]]:
        """Extract intelligence from multiple messages."""
        all_intelligence = {
            "upi_ids": set(),
            "phone_numbers": set(),
            "urls": set()
        }
        
        for message in messages:
            intel = cls.extract(message)
            all_intelligence["upi_ids"].update(intel["upi_ids"])
            all_intelligence["phone_numbers"].update(intel["phone_numbers"])
            all_intelligence["urls"].update(intel["urls"])
        
        return {
            "upi_ids": list(all_intelligence["upi_ids"]),
            "phone_numbers": list(all_intelligence["phone_numbers"]),
            "urls": list(all_intelligence["urls"])
        }
