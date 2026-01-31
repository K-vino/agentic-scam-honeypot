import random
from typing import List, Optional


class ReplyGenerator:
    """Generates human-like replies to engage scammers."""
    
    # Response templates categorized by engagement stage
    INITIAL_RESPONSES = [
        "Hi, I received your message. Can you tell me more?",
        "Hello! What is this about?",
        "I'm interested. Please explain.",
        "Yes, I'm here. What do you need?",
        "Got your message. What should I do next?",
    ]
    
    CURIOUS_RESPONSES = [
        "That sounds interesting. How does it work?",
        "Can you provide more details?",
        "I want to know more about this.",
        "What are the next steps?",
        "How do I proceed with this?",
    ]
    
    VERIFICATION_REQUESTS = [
        "Can you send me the link?",
        "What's the website?",
        "Where should I make the payment?",
        "What's your UPI ID?",
        "Can you share your contact number?",
        "How can I reach you?",
    ]
    
    HESITANT_RESPONSES = [
        "Is this legitimate? How do I know?",
        "I'm not sure about this. Can you verify?",
        "This seems unusual. Are you sure?",
        "I need some time to think about it.",
        "Can you prove this is real?",
    ]
    
    ENGAGED_RESPONSES = [
        "Okay, I'm ready. What should I do?",
        "Yes, I want to proceed. Guide me.",
        "I'm interested. Let's do this.",
        "Alright, tell me what to do next.",
        "I'm convinced. How do we continue?",
    ]
    
    STALLING_RESPONSES = [
        "Just a moment, I need to check something.",
        "Can you wait? I'm busy right now.",
        "Let me get back to you in a few minutes.",
        "I need to talk to my family first.",
        "Hold on, I'm having network issues.",
    ]
    
    @classmethod
    def generate_reply(cls, message_count: int, last_message: str) -> str:
        """
        Generate a human-like reply based on conversation stage.
        
        Args:
            message_count: Number of messages in the conversation
            last_message: The last message from the scammer
            
        Returns:
            A contextual human-like reply
        """
        message_lower = last_message.lower()
        
        # Initial response
        if message_count <= 1:
            return random.choice(cls.INITIAL_RESPONSES)
        
        # If scammer is asking for payment/transfer
        if any(word in message_lower for word in ["pay", "payment", "transfer", "send", "money"]):
            if message_count < 4:
                return random.choice(cls.VERIFICATION_REQUESTS)
            else:
                return random.choice(cls.HESITANT_RESPONSES)
        
        # If scammer is providing links/details
        if any(word in message_lower for word in ["link", "website", "click", "upi", "account"]):
            return random.choice(cls.ENGAGED_RESPONSES)
        
        # Mid-conversation engagement
        if message_count <= 3:
            return random.choice(cls.CURIOUS_RESPONSES)
        elif message_count <= 6:
            return random.choice(cls.VERIFICATION_REQUESTS)
        elif message_count <= 9:
            return random.choice(cls.ENGAGED_RESPONSES)
        else:
            # Start stalling to extract more information
            return random.choice(cls.STALLING_RESPONSES)
    
    @classmethod
    def should_end_conversation(cls, message_count: int) -> bool:
        """Determine if the conversation should end."""
        # End conversation after 12-15 exchanges
        return message_count >= 12
