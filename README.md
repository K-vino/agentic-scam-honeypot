# Agentic Scam Honeypot

Backend REST API that detects scam messages, engages scammers using an autonomous agent, extracts scam intelligence such as UPI IDs and phishing links, and prepares structured reports for analysis and evaluation.

## Features

- **API Key Authentication**: Secure endpoints with API key-based authentication
- **Session Management**: Track conversations with unique session IDs (in-memory, no database)
- **Scam Detection**: Rule-based detection for multiple scam types:
  - Financial fraud
  - Phishing
  - UPI scams
  - Fake prizes
  - Job scams
  - Romance scams
  - Tech support scams
- **Human-like Replies**: Context-aware reply generation to engage scammers naturally
- **Intelligence Extraction**: Automatic extraction of:
  - UPI IDs
  - Phone numbers
  - URLs
  - Bank account details
  - Email addresses
- **Callback System**: Structured callbacks when engagement completes

## Installation

1. Clone the repository:
```bash
git clone https://github.com/K-vino/agentic-scam-honeypot.git
cd agentic-scam-honeypot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Configuration

Edit `.env` file to configure:

- `API_KEY`: Your secret API key for authentication
- `CALLBACK_URL`: (Optional) URL to receive callbacks when sessions complete
- `MAX_MESSAGES_PER_SESSION`: Maximum messages before session terminates (default: 20)
- `SESSION_TIMEOUT_SECONDS`: Session timeout in seconds (default: 3600)

## Usage

### Start the server

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or using the main module:

```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

### API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Example Request

Send a scam message:

```bash
curl -X POST "http://localhost:8000/api/v1/message" \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "session-123",
    "message": "Congratulations! You have won a prize of Rs 50,000. Send your UPI ID to claim: winner@paytm"
  }'
```

Response:

```json
{
  "sessionId": "session-123",
  "reply": "Really? I won something? That's amazing!",
  "scamDetected": true,
  "scamIntents": ["fake_prize", "upi_scam"],
  "confidence": 0.85,
  "shouldContinue": true,
  "extractedIntelligence": {
    "upiIds": ["winner@paytm"],
    "phoneNumbers": [],
    "urls": [],
    "bankDetails": [],
    "emailAddresses": []
  }
}
```

### Health Check

```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

### Cleanup Expired Sessions

```bash
curl -X POST "http://localhost:8000/api/v1/cleanup" \
  -H "X-API-Key: your-secret-api-key-here"
```

## Architecture

```
app/
├── main.py                 # FastAPI application entry point
├── core/
│   ├── config.py          # Configuration and settings
│   └── security.py        # API key authentication
├── models/
│   └── schemas.py         # Pydantic models
├── api/
│   └── routes.py          # API endpoints
└── services/
    ├── session_manager.py     # Session management
    ├── scam_detector.py       # Scam detection logic
    ├── intelligence_extractor.py  # Intelligence extraction
    ├── reply_generator.py     # Reply generation
    └── callback_service.py    # Callback handling
```

## Session Lifecycle

1. **Message Receipt**: API receives a message with a sessionId
2. **Scam Detection**: Rule-based analysis detects scam intent
3. **Intelligence Extraction**: Extracts UPI IDs, phone numbers, URLs, etc.
4. **Reply Generation**: Generates contextual human-like reply
5. **Session Update**: Updates session state and history
6. **Termination Check**: Checks if session should end (max messages, timeout)
7. **Callback**: Sends structured callback when engagement completes

## Session Termination

Sessions terminate when:
- Maximum messages reached (default: 20)
- Session timeout (default: 1 hour of inactivity)
- Manually terminated

Upon termination, a callback is sent (if configured) with:
- Complete conversation history
- Detected scam intents
- Confidence scores
- Extracted intelligence
- Session metadata

## Security

- API key authentication required for all endpoints
- No database, no data persistence
- Session data stored in memory only
- Configurable session timeouts

## Development

Run tests:
```bash
pytest tests/
```

## License

See LICENSE file for details.
