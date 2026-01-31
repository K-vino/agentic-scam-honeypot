# agentic-scam-honeypot

Backend REST API that detects scam messages, engages scammers using an autonomous agent, extracts scam intelligence such as UPI IDs and phishing links, and prepares structured reports for analysis and evaluation.

## Features

- **Scam Detection**: Rule-based scam intent detection using keywords and patterns
- **Session Management**: Track conversation state using sessionId (in-memory, no database)
- **API Key Authentication**: Secure endpoints with API key authentication
- **Intelligence Extraction**: Extract UPI IDs, phone numbers, and URLs from messages
- **Human-like Replies**: Generate contextual, engaging responses to scammers
- **Callback System**: Send structured reports when conversations end

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

3. Create a `.env` file from the example:
```bash
cp .env.example .env
```

4. Update the `.env` file with your configuration:
```env
API_KEY=your-secure-api-key-here
API_HOST=0.0.0.0
API_PORT=8000
CALLBACK_URL=https://your-callback-endpoint.com/webhook
```

## Running the Server

Start the FastAPI server:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /api/message

Process incoming scam messages and generate replies.

**Headers:**
```
X-API-Key: your-api-key
```

**Request Body:**
```json
{
  "session_id": "session-123",
  "message": "Congratulations! You have won 1 crore rupees. Click here to claim: http://scam-link.com",
  "metadata": {
    "source": "whatsapp"
  }
}
```

**Response:**
```json
{
  "session_id": "session-123",
  "reply": "That sounds interesting. How does it work?",
  "is_scam": true,
  "confidence": 0.85,
  "intelligence": {
    "upi_ids": [],
    "phone_numbers": [],
    "urls": ["http://scam-link.com"]
  },
  "session_ended": false
}
```

### GET /api/session/{session_id}

Get details about a specific session.

**Headers:**
```
X-API-Key: your-api-key
```

**Response:**
```json
{
  "session_id": "session-123",
  "messages": [...],
  "intelligence": {...},
  "is_scam_confirmed": true,
  "created_at": "2026-01-31T03:51:07.000Z",
  "last_activity": "2026-01-31T03:52:15.000Z",
  "message_count": 5
}
```

### DELETE /api/session/{session_id}

Manually end a session and trigger callback.

**Headers:**
```
X-API-Key: your-api-key
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "active_sessions": 3
}
```

## Callback System

When a conversation ends (after ~12 messages or manual termination), the system sends a POST request to the configured `CALLBACK_URL` with the following payload:

```json
{
  "session_id": "session-123",
  "message_count": 12,
  "intelligence": {
    "upi_ids": ["scammer@paytm"],
    "phone_numbers": ["9876543210"],
    "urls": ["http://phishing-site.com"]
  },
  "messages": [
    {
      "role": "scammer",
      "content": "...",
      "timestamp": "2026-01-31T03:51:07.000Z"
    },
    {
      "role": "bot",
      "content": "...",
      "timestamp": "2026-01-31T03:51:10.000Z"
    }
  ],
  "is_scam_confirmed": true,
  "created_at": "2026-01-31T03:51:07.000Z",
  "last_activity": "2026-01-31T03:55:00.000Z"
}
```

## Example Usage

```bash
# Send a scam message
curl -X POST http://localhost:8000/api/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secure-api-key-here" \
  -d '{
    "session_id": "test-session-1",
    "message": "Urgent! Your bank account will be blocked. Verify now at http://fake-bank.com or call 9876543210"
  }'
```

## Architecture

```
┌─────────────────┐
│  Scam Message   │
│  (via API)      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│           FastAPI Backend (main.py)             │
│  ┌───────────────────────────────────────────┐  │
│  │  API Key Authentication                   │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────┐  ┌──────────────┐            │
│  │ Scam         │  │ Intelligence │            │
│  │ Detector     │  │ Extractor    │            │
│  │ (Rules)      │  │ (UPI, Phone, │            │
│  │              │  │  URLs)       │            │
│  └──────────────┘  └──────────────┘            │
│                                                  │
│  ┌──────────────┐  ┌──────────────┐            │
│  │ Reply        │  │ Session      │            │
│  │ Generator    │  │ Manager      │            │
│  │ (Human-like) │  │ (In-memory)  │            │
│  └──────────────┘  └──────────────┘            │
└─────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Response + Intelligence    │
│  + Human-like Reply         │
└─────────────────────────────┘
         │
         ▼ (When session ends)
┌─────────────────────────────┐
│  Callback with Full Report  │
│  (to configured endpoint)   │
└─────────────────────────────┘
```

### Components

- **main.py**: FastAPI application with endpoints and authentication
- **session_manager.py**: In-memory session management
- **scam_detector.py**: Rule-based scam detection logic
- **reply_generator.py**: Human-like response generation
- **intelligence_extractor.py**: Entity extraction (UPI IDs, phone numbers, URLs)

## Security

- API key authentication on all endpoints
- No data persistence (in-memory only)
- No database required
- Sensitive information only in environment variables

## License

See LICENSE file for details.
