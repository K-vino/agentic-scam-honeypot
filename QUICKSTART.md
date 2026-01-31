# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment (optional)
cp .env.example .env
# Edit .env to set your API_KEY and other settings
```

## Running the Server

```bash
# Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Quick Test

### Using cURL

```bash
# Test with a scam message
curl -X POST http://localhost:8000/api/v1/message \
  -H "X-API-Key: default-api-key-change-me" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "test-001",
    "message": "Congratulations! You won Rs 50,000. Send UPI to winner@paytm"
  }'
```

### Using the Demo Script

```bash
# Run comprehensive demo
python demo.py
```

## Key Endpoints

- `POST /api/v1/message` - Send scam message (requires API key)
- `GET /api/v1/health` - Check API health
- `POST /api/v1/cleanup` - Cleanup expired sessions (requires API key)

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app
```

## Features Demonstrated

1. **API Key Authentication** - All endpoints protected
2. **Scam Detection** - Multiple scam types detected:
   - Financial fraud
   - Phishing
   - UPI scams
   - Fake prizes
   - Job scams
   - Romance scams
   - Tech support scams

3. **Intelligence Extraction**:
   - UPI IDs
   - Phone numbers
   - URLs
   - Bank account numbers
   - Email addresses

4. **Session Management**:
   - In-memory session tracking
   - Automatic expiration
   - Conversation history

5. **Human-like Replies**:
   - Context-aware responses
   - Natural engagement
   - Progressive interaction

6. **Callback System**:
   - Structured data on completion
   - Configurable webhook URL

## Configuration Options

Edit `.env` file:

```env
# API Authentication
API_KEY=your-secret-key

# Session Limits
MAX_MESSAGES_PER_SESSION=20
SESSION_TIMEOUT_SECONDS=3600

# Callback (optional)
CALLBACK_URL=https://your-webhook-url.com/callback
```

## Production Deployment

For production use:

1. Change the default API key
2. Use environment variables for sensitive data
3. Configure callback URL for notifications
4. Consider adding rate limiting
5. Set up proper logging and monitoring
6. Use a production ASGI server like Gunicorn

```bash
# Example production command
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
