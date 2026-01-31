# API Usage Examples

This document provides practical examples for using the Agentic Scam Honeypot API.

## Setup

1. Start the server:
```bash
python main.py
```

2. The API will be available at `http://localhost:8000`

## Example 1: Basic Scam Message Processing

### Request
```bash
curl -X POST http://localhost:8000/api/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: default-api-key" \
  -d '{
    "session_id": "session-001",
    "message": "Congratulations! You have won 10 lakh rupees in KBC lottery. Click here to claim: http://fake-kbc.com"
  }'
```

### Response
```json
{
  "session_id": "session-001",
  "reply": "Hi, I received your message. Can you tell me more?",
  "is_scam": true,
  "confidence": 1.0,
  "intelligence": {
    "upi_ids": [],
    "phone_numbers": [],
    "urls": ["http://fake-kbc.com"]
  },
  "session_ended": false
}
```

## Example 2: Multi-Turn Conversation

### Turn 1 - Initial Contact
```bash
curl -X POST http://localhost:8000/api/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: default-api-key" \
  -d '{
    "session_id": "session-002",
    "message": "Your account will be suspended! Verify immediately."
  }'
```

### Turn 2 - Scammer Provides Details
```bash
curl -X POST http://localhost:8000/api/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: default-api-key" \
  -d '{
    "session_id": "session-002",
    "message": "Send verification fee of 500 rupees to secure@paytm or call 9876543210"
  }'
```

### Response (Turn 2)
```json
{
  "session_id": "session-002",
  "reply": "What's your UPI ID?",
  "is_scam": true,
  "confidence": 0.8,
  "intelligence": {
    "upi_ids": ["secure@paytm"],
    "phone_numbers": ["9876543210"],
    "urls": []
  },
  "session_ended": false
}
```

## Example 3: Extracting Intelligence

The API automatically extracts:
- **UPI IDs**: Pattern like `username@provider`
- **Phone Numbers**: 10-digit Indian numbers (with or without +91)
- **URLs**: HTTP/HTTPS links and www. prefixes

### Request with Multiple Intelligence Items
```bash
curl -X POST http://localhost:8000/api/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: default-api-key" \
  -d '{
    "session_id": "session-003",
    "message": "Transfer amount to winner123@paytm, call +91-9123456789, or visit https://phishing-bank.com and www.fake-lottery.net for verification"
  }'
```

### Response
```json
{
  "session_id": "session-003",
  "reply": "Can you send me the link?",
  "is_scam": true,
  "confidence": 0.6,
  "intelligence": {
    "upi_ids": ["winner123@paytm"],
    "phone_numbers": ["9123456789"],
    "urls": ["https://phishing-bank.com", "www.fake-lottery.net"]
  },
  "session_ended": false
}
```

## Example 4: Checking Session Details

### Request
```bash
curl http://localhost:8000/api/session/session-002 \
  -H "X-API-Key: default-api-key"
```

### Response
```json
{
  "session_id": "session-002",
  "messages": [
    {
      "role": "scammer",
      "content": "Your account will be suspended! Verify immediately.",
      "timestamp": "2026-01-31T03:51:07.000Z"
    },
    {
      "role": "bot",
      "content": "Hello! What is this about?",
      "timestamp": "2026-01-31T03:51:08.000Z"
    },
    {
      "role": "scammer",
      "content": "Send verification fee of 500 rupees to secure@paytm or call 9876543210",
      "timestamp": "2026-01-31T03:51:15.000Z"
    },
    {
      "role": "bot",
      "content": "What's your UPI ID?",
      "timestamp": "2026-01-31T03:51:15.000Z"
    }
  ],
  "intelligence": {
    "upi_ids": ["secure@paytm"],
    "phone_numbers": ["9876543210"],
    "urls": []
  },
  "is_scam_confirmed": true,
  "created_at": "2026-01-31T03:51:07.000Z",
  "last_activity": "2026-01-31T03:51:15.000Z",
  "message_count": 4
}
```

## Example 5: Manually Ending a Session

### Request
```bash
curl -X DELETE http://localhost:8000/api/session/session-002 \
  -H "X-API-Key: default-api-key"
```

### Response
```json
{
  "message": "Session ended",
  "session_id": "session-002"
}
```

This will also trigger the callback to the configured `CALLBACK_URL` with the complete session data.

## Example 6: Callback Payload

When a session ends (either automatically after ~12 messages or manually), the API sends a POST request to the configured `CALLBACK_URL`:

```json
{
  "session_id": "session-002",
  "message_count": 12,
  "intelligence": {
    "upi_ids": ["scammer@paytm", "fraudster@upi"],
    "phone_numbers": ["9876543210", "9123456789"],
    "urls": ["http://phishing-site.com", "www.fake-bank.net"]
  },
  "messages": [
    {
      "role": "scammer",
      "content": "Your account will be suspended!",
      "timestamp": "2026-01-31T03:51:07.000Z"
    },
    {
      "role": "bot",
      "content": "What should I do?",
      "timestamp": "2026-01-31T03:51:08.000Z"
    }
  ],
  "is_scam_confirmed": true,
  "created_at": "2026-01-31T03:51:07.000Z",
  "last_activity": "2026-01-31T03:55:00.000Z"
}
```

## Example 7: Health Check

### Request
```bash
curl http://localhost:8000/health
```

### Response
```json
{
  "status": "healthy",
  "active_sessions": 5
}
```

## Error Handling

### Missing API Key
```bash
curl -X POST http://localhost:8000/api/message \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test", "message": "test"}'
```

**Response (422):**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["header", "x-api-key"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

### Invalid API Key
```bash
curl -X POST http://localhost:8000/api/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: wrong-key" \
  -d '{"session_id": "test", "message": "test"}'
```

**Response (401):**
```json
{
  "detail": "Invalid API key"
}
```

### Session Not Found
```bash
curl http://localhost:8000/api/session/nonexistent \
  -H "X-API-Key: default-api-key"
```

**Response (404):**
```json
{
  "detail": "Session not found"
}
```

## Python Client Example

```python
import requests
import json

API_BASE_URL = "http://localhost:8000"
API_KEY = "default-api-key"

def send_message(session_id: str, message: str):
    """Send a message to the honeypot API."""
    response = requests.post(
        f"{API_BASE_URL}/api/message",
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY
        },
        json={
            "session_id": session_id,
            "message": message
        }
    )
    return response.json()

def get_session(session_id: str):
    """Get session details."""
    response = requests.get(
        f"{API_BASE_URL}/api/session/{session_id}",
        headers={"X-API-Key": API_KEY}
    )
    return response.json()

# Example usage
if __name__ == "__main__":
    # Send first message
    result = send_message(
        "python-client-test",
        "Congratulations! You won 1 crore rupees. Call 9876543210 to claim."
    )
    print("Bot reply:", result["reply"])
    print("Scam detected:", result["is_scam"])
    print("Intelligence extracted:", result["intelligence"])
    
    # Check session details
    session = get_session("python-client-test")
    print(f"Total messages: {session['message_count']}")
```

## Testing Scam Detection

The system detects scams based on:
- **Keywords**: urgent, verify, account, suspended, lottery, winner, prize, etc.
- **Patterns**: "click here", "verify now", "account suspended", etc.

### High Confidence Scam (confidence > 0.8)
```json
{
  "message": "URGENT! Your bank account suspended. Verify now at http://fake-bank.com or lose access permanently!"
}
```

### Medium Confidence (confidence 0.3-0.8)
```json
{
  "message": "You have won a prize. Please claim it soon."
}
```

### Low/No Scam Detection (confidence < 0.3)
```json
{
  "message": "Hello, how are you doing today?"
}
```
