# Deployment Guide

This guide explains how to deploy the Agentic Scam Honeypot API in different environments.

## Local Development

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/K-vino/agentic-scam-honeypot.git
cd agentic-scam-honeypot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Edit `.env` with your configuration:
```env
API_KEY=your-secure-api-key-here
API_HOST=0.0.0.0
API_PORT=8000
CALLBACK_URL=https://your-callback-endpoint.com/webhook
```

5. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Production Deployment

### Option 1: Using Uvicorn Directly

Run with production settings:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Option 2: Using Gunicorn with Uvicorn Workers

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Option 3: Using Docker

1. Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Create `.dockerignore`:
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.git
.gitignore
*.md
```

3. Build and run:
```bash
docker build -t scam-honeypot .
docker run -p 8000:8000 --env-file .env scam-honeypot
```

### Option 4: Using Docker Compose

1. Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
```

2. Run:
```bash
docker-compose up -d
```

## Cloud Deployment

### Deploying to AWS (EC2)

1. Launch an EC2 instance (Ubuntu 22.04)
2. SSH into the instance
3. Install Python and dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv
```

4. Clone and setup the application:
```bash
git clone https://github.com/K-vino/agentic-scam-honeypot.git
cd agentic-scam-honeypot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Create and configure `.env` file

6. Run with systemd service:

Create `/etc/systemd/system/scam-honeypot.service`:
```ini
[Unit]
Description=Agentic Scam Honeypot API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/agentic-scam-honeypot
Environment="PATH=/home/ubuntu/agentic-scam-honeypot/venv/bin"
ExecStart=/home/ubuntu/agentic-scam-honeypot/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable scam-honeypot
sudo systemctl start scam-honeypot
```

### Deploying to Google Cloud Platform (Cloud Run)

1. Install Google Cloud SDK

2. Create `Dockerfile` (see Docker option above)

3. Build and deploy:
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/scam-honeypot
gcloud run deploy scam-honeypot --image gcr.io/PROJECT-ID/scam-honeypot --platform managed
```

### Deploying to Heroku

1. Create `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Create `runtime.txt`:
```
python-3.11.0
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

4. Set environment variables:
```bash
heroku config:set API_KEY=your-api-key
heroku config:set CALLBACK_URL=your-callback-url
```

### Deploying to Azure (App Service)

1. Install Azure CLI

2. Create App Service:
```bash
az webapp up --name scam-honeypot --runtime "PYTHON:3.11"
```

3. Configure environment variables:
```bash
az webapp config appsettings set --name scam-honeypot --settings API_KEY=your-key CALLBACK_URL=your-url
```

## Security Considerations

### API Key Management
- Use strong, randomly generated API keys
- Store keys securely using environment variables or secret managers
- Rotate keys periodically
- Never commit keys to version control

### HTTPS/TLS
- Always use HTTPS in production
- Use a reverse proxy (nginx, Caddy) for TLS termination
- Example nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Rate Limiting
Consider adding rate limiting using:
- Nginx rate limiting
- FastAPI middleware (slowapi)
- Cloud provider rate limiting (AWS API Gateway, GCP Cloud Armor)

### Monitoring
- Monitor API health using `/health` endpoint
- Set up alerts for high error rates
- Track active sessions and memory usage
- Use logging for debugging (FastAPI has built-in logging)

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `API_KEY` | Yes | `default-api-key` | API authentication key |
| `API_HOST` | No | `0.0.0.0` | Host to bind the server |
| `API_PORT` | No | `8000` | Port to bind the server |
| `CALLBACK_URL` | No | None | URL to send completion callbacks |

## Performance Tuning

### Uvicorn Workers
For production, use multiple workers:
```bash
uvicorn main:app --workers 4
```

### Memory Management
Since sessions are stored in-memory:
- Monitor memory usage
- Consider implementing session cleanup for old/inactive sessions
- Set resource limits in containerized environments

### Scaling
The API is stateless except for in-memory sessions:
- For horizontal scaling, implement distributed session storage (Redis, Memcached)
- Use a load balancer to distribute traffic
- Current implementation is suitable for single-instance deployments

## Troubleshooting

### Server won't start
- Check if port 8000 is already in use: `lsof -i :8000`
- Verify all dependencies are installed: `pip list`
- Check Python version: `python --version`

### API returns 500 errors
- Check server logs: `tail -f /tmp/server.log`
- Verify environment variables are set correctly
- Test individual modules: `python test_honeypot.py`

### Callbacks not working
- Verify `CALLBACK_URL` is set in `.env`
- Check network connectivity to callback endpoint
- Review server logs for callback errors
- Test callback endpoint independently

## Backup and Recovery

Since this system uses in-memory storage:
- No database backup required
- Session data is lost on restart (by design)
- Configuration is in `.env` file (backup this file)
- Code is version controlled in Git

## Updates and Maintenance

### Updating the Application
```bash
git pull origin main
pip install -r requirements.txt
# Restart the service
sudo systemctl restart scam-honeypot
```

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Running Tests
```bash
python test_honeypot.py
```
