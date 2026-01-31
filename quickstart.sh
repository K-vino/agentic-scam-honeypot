#!/bin/bash
# Quick start script for the Agentic Scam Honeypot API

echo "===================================="
echo "Agentic Scam Honeypot - Quick Start"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo "⚠️  Please edit .env and set your API_KEY and CALLBACK_URL"
    echo ""
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt > /tmp/install.log 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies. Check /tmp/install.log for details."
    exit 1
fi
echo ""

# Run tests
echo "Running tests..."
python test_honeypot.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ All tests passed!"
else
    echo ""
    echo "❌ Some tests failed. Please check the output above."
    exit 1
fi
echo ""

# Start server
echo "===================================="
echo "Starting server..."
echo "===================================="
echo ""
echo "The API will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
