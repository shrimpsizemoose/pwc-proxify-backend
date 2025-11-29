#!/bin/bash
# Quick start script for Meeting Prep Assistant API

echo "🚀 Starting Meeting Prep Assistant API..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env and add your OPENAI_API_KEY"
    echo "   nano .env"
    exit 1
fi

# Check if OPENAI_API_KEY is set
if ! grep -q "OPENAI_API_KEY=sk-" .env; then
    echo "⚠️  OPENAI_API_KEY not configured in .env"
    echo "📝 Please edit .env and add your OpenAI API key"
    exit 1
fi

# Run the server
echo "✅ Starting server on http://localhost:30903"
echo "📚 API Docs: http://localhost:30903/docs"
echo ""

uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 30903
