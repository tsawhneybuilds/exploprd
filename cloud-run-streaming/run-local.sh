#!/bin/bash

# Local development script for Chat-PRD Streaming Service
echo "🚀 Starting Chat-PRD Streaming Service locally..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file template..."
    cat > .env << EOF
# Copy your OpenAI API key here
OPENAI_API_KEY=your-openai-api-key-here

# Your Google Cloud Project ID (optional for local testing)
GOOGLE_CLOUD_PROJECT=your-project-id-here

# Local server port
PORT=8080
EOF
    echo "⚠️  Please edit .env file and add your OpenAI API key!"
    echo "   Then run this script again."
    exit 1
fi

# Check if API key is set
source .env
if [ "$OPENAI_API_KEY" = "your-openai-api-key-here" ]; then
    echo "❌ Please set your OpenAI API key in the .env file!"
    echo "   Edit .env and replace 'your-openai-api-key-here' with your actual API key."
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "📦 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "🌟 Starting server at http://localhost:8080"
echo "📋 Health check: http://localhost:8080/health"
echo "🧪 Test with: python test-local.py"
echo ""
echo "Press Ctrl+C to stop"

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8080 --reload 