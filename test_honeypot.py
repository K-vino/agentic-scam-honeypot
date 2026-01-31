#!/usr/bin/env python3
"""
Test script for the Agentic Scam Honeypot API
"""
import sys
from scam_detector import ScamDetector
from intelligence_extractor import IntelligenceExtractor
from reply_generator import ReplyGenerator
from session_manager import SessionManager


def test_scam_detector():
    """Test scam detection functionality."""
    print("Testing Scam Detector...")
    
    # Test obvious scam
    scam_msg = "Congratulations! You won 1 crore. Click here to claim your prize!"
    result = ScamDetector.detect_scam(scam_msg)
    assert result["is_scam"] == True, "Should detect obvious scam"
    assert result["confidence"] > 0.5, "Should have high confidence for obvious scam"
    print(f"✓ Detected scam with confidence {result['confidence']}")
    
    # Test normal message
    normal_msg = "Hello, how are you?"
    result = ScamDetector.detect_scam(normal_msg)
    assert result["is_scam"] == False, "Should not detect normal message as scam"
    print(f"✓ Correctly identified normal message (confidence: {result['confidence']})")
    
    print("Scam Detector tests passed!\n")


def test_intelligence_extractor():
    """Test intelligence extraction functionality."""
    print("Testing Intelligence Extractor...")
    
    # Test UPI ID extraction
    msg = "Send payment to scammer@paytm"
    intel = IntelligenceExtractor.extract(msg)
    assert "scammer@paytm" in intel["upi_ids"], "Should extract UPI ID"
    print(f"✓ Extracted UPI ID: {intel['upi_ids']}")
    
    # Test phone number extraction
    msg = "Call me at 9876543210 or +91-9123456789"
    intel = IntelligenceExtractor.extract(msg)
    assert len(intel["phone_numbers"]) >= 1, "Should extract phone numbers"
    print(f"✓ Extracted phone numbers: {intel['phone_numbers']}")
    
    # Test URL extraction
    msg = "Visit http://scam.com and www.phishing.net for details"
    intel = IntelligenceExtractor.extract(msg)
    assert len(intel["urls"]) >= 1, "Should extract URLs"
    print(f"✓ Extracted URLs: {intel['urls']}")
    
    print("Intelligence Extractor tests passed!\n")


def test_reply_generator():
    """Test reply generation functionality."""
    print("Testing Reply Generator...")
    
    # Test initial reply
    reply = ReplyGenerator.generate_reply(1, "Hello")
    assert len(reply) > 0, "Should generate reply"
    print(f"✓ Generated initial reply: '{reply}'")
    
    # Test mid-conversation reply
    reply = ReplyGenerator.generate_reply(5, "Send money now")
    assert len(reply) > 0, "Should generate reply"
    print(f"✓ Generated mid-conversation reply: '{reply}'")
    
    # Test conversation ending
    should_end = ReplyGenerator.should_end_conversation(15)
    assert should_end == True, "Should end after many messages"
    print("✓ Correctly determines when to end conversation")
    
    print("Reply Generator tests passed!\n")


def test_session_manager():
    """Test session management functionality."""
    print("Testing Session Manager...")
    
    manager = SessionManager()
    
    # Test session creation
    session = manager.create_session("test-123")
    assert session.session_id == "test-123", "Should create session with correct ID"
    print("✓ Created session successfully")
    
    # Test adding messages
    session.add_message("scammer", "Send money to evil@bank")
    assert session.get_message_count() == 1, "Should have 1 message"
    assert len(session.intelligence["upi_ids"]) > 0, "Should extract intelligence from message"
    print(f"✓ Added message and extracted intelligence: {session.intelligence}")
    
    # Test session retrieval
    retrieved = manager.get_session("test-123")
    assert retrieved is not None, "Should retrieve existing session"
    assert retrieved.session_id == "test-123", "Should retrieve correct session"
    print("✓ Retrieved session successfully")
    
    # Test session ending
    session.end_session()
    assert session.is_active == False, "Session should be inactive"
    print("✓ Ended session successfully")
    
    print("Session Manager tests passed!\n")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Running Agentic Scam Honeypot Tests")
    print("=" * 60 + "\n")
    
    try:
        test_scam_detector()
        test_intelligence_extractor()
        test_reply_generator()
        test_session_manager()
        
        print("=" * 60)
        print("✅ All tests passed successfully!")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
