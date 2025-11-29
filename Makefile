.PHONY: help install setup run test clean demo start

# Default target
help:
	@echo "Meeting Prep Assistant - Makefile Commands"
	@echo "==========================================="
	@echo ""
	@echo "Setup & Run:"
	@echo "  make start         - Quick start guide (checks everything)"
	@echo "  make install       - Install dependencies with uv"
	@echo "  make setup         - Create .env file from template"
	@echo "  make run           - Start the API server"
	@echo "  make test          - Run setup verification"
	@echo ""
	@echo "Demo & Examples:"
	@echo "  make demo          - Run complete demo flow"
	@echo "  make demo-brief    - Generate meeting brief for GreenTech"
	@echo "  make demo-clients  - List all clients"
	@echo "  make demo-client   - Get GreenTech client details"
	@echo "  make demo-comms    - Search GreenTech communications"
	@echo "  make demo-actions  - Get GreenTech action items"
	@echo "  make demo-kb       - Ask knowledge base about ESG"
	@echo "  make demo-topics   - List knowledge base topics"
	@echo "  make demo-docs     - Get document summaries"
	@echo ""
	@echo "API Examples (individual):"
	@echo "  make ex-list       - List all clients"
	@echo "  make ex-client     - Get client details"
	@echo "  make ex-brief      - Generate meeting brief"
	@echo "  make ex-search     - Search communications"
	@echo "  make ex-actions    - Get action items"
	@echo "  make ex-kb-ask     - Ask knowledge base"
	@echo "  make ex-kb-search  - Search knowledge base"
	@echo "  make ex-kb-topics  - List topics"
	@echo "  make ex-docs-list  - List documents"
	@echo "  make ex-docs-sum   - Get document summaries"
	@echo ""
	@echo "Docker (Local Build):"
	@echo "  make docker-build    - Build Docker image locally"
	@echo "  make docker-run      - Run with Docker Compose (local build)"
	@echo "  make docker-stop     - Stop Docker containers"
	@echo "  make docker-logs     - View Docker logs"
	@echo ""
	@echo "Docker (GitHub Container Registry):"
	@echo "  make docker-pull       - Pull latest image from GHCR"
	@echo "  make docker-run-ghcr   - Run with pre-built GHCR image"
	@echo "  make docker-stop-ghcr  - Stop GHCR containers"
	@echo "  make docker-logs-ghcr  - View GHCR container logs"
	@echo ""
	@echo "Docker (Other):"
	@echo "  make docker-shell    - Open shell in container"
	@echo "  make docker-clean    - Remove Docker containers and images"
	@echo ""
	@echo "Utilities:"
	@echo "  make health        - Check API health"
	@echo "  make clean         - Clean cache files"
	@echo "  make logs          - Show recent logs (if running)"
	@echo ""

# API base URL
API_URL = http://localhost:30903

# Check if API is running
check-api:
	@echo "🔍 Checking if API is running..."
	@if ! curl -s $(API_URL)/health > /dev/null 2>&1; then \
		echo ""; \
		echo "❌ API is not running!"; \
		echo ""; \
		echo "Start it in another terminal with:"; \
		echo "  make run"; \
		echo ""; \
		echo "Or with Docker:"; \
		echo "  make docker-run"; \
		echo ""; \
		exit 1; \
	fi
	@echo "✅ API is running!"
	@echo ""

#############################################
# Setup & Installation
#############################################

install:
	@echo "📦 Installing dependencies with uv..."
	uv sync
	@echo "✅ Dependencies installed!"

setup:
	@if [ ! -f .env ]; then \
		echo "📝 Creating .env file..."; \
		cp .env.example .env; \
		echo "⚠️  Please edit .env and add your OPENAI_API_KEY"; \
		echo "   nano .env"; \
	else \
		echo "✅ .env file already exists"; \
	fi

run:
	@echo "🚀 Starting API server..."
	@echo "📚 API Docs: http://localhost:30903/docs"
	@echo ""
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 30903

test:
	@echo "🧪 Running setup verification..."
	uv run python test_setup.py

start:
	@echo "🚀 Meeting Prep Assistant - Quick Start"
	@echo "========================================"
	@echo ""
	@echo "Checking your setup..."
	@echo ""
	@if ! curl -s $(API_URL)/health > /dev/null 2>&1; then \
		echo "❌ API is not running"; \
		echo ""; \
		echo "📋 To start the API:"; \
		echo ""; \
		echo "Option 1: In this terminal (blocks)"; \
		echo "  make run"; \
		echo ""; \
		echo "Option 2: In another terminal"; \
		echo "  # Terminal 1:"; \
		echo "  make run"; \
		echo "  # Terminal 2 (this one):"; \
		echo "  make demo"; \
		echo ""; \
		echo "Option 3: With Docker (background)"; \
		echo "  make docker-build"; \
		echo "  make docker-run"; \
		echo "  make demo"; \
		echo ""; \
		exit 1; \
	else \
		echo "✅ API is running at $(API_URL)"; \
		echo ""; \
		echo "🎯 Try these commands:"; \
		echo "  make demo          # Complete demo"; \
		echo "  make demo-brief    # Meeting brief"; \
		echo "  make demo-kb       # Knowledge Q&A"; \
		echo ""; \
		echo "📚 API Docs: http://localhost:30903/docs"; \
		echo ""; \
	fi

#############################################
# Complete Demo Flow
#############################################

demo: check-api
	@echo "🎬 Running Demo (Working Features)"
	@echo "===================================="
	@echo ""
	@echo "1️⃣  Listing all clients..."
	@response=$$(curl -s $(API_URL)/clients/list); \
	if echo "$$response" | jq empty 2>/dev/null; then \
		echo "$$response" | jq -r '.[] | "  - \(.AccountName) (\(.Industry), \(.Region))"'; \
	else \
		echo "❌ Error from API:"; \
		echo "$$response"; \
		exit 1; \
	fi
	@echo ""
	@echo "2️⃣  Checking API Info..."
	@curl -s $(API_URL)/ | jq '.'
	@echo ""
	@echo "3️⃣  Testing Knowledge Base Topics..."
	@curl -s $(API_URL)/knowledge/topics 2>&1 | head -20
	@echo ""
	@echo "✅ Demo Complete!"
	@echo ""
	@echo "📚 Full API docs: http://localhost:30903/docs"
	@echo "💡 Note: Some endpoints need data relationship fixes (see QUICKFIX.md)"

#############################################
# Individual Demo Commands
#############################################

demo-brief: check-api
	@echo "📋 Generating Meeting Brief for GreenTech..."
	@echo ""
	@curl -s -X POST $(API_URL)/clients/GreenTech/meeting-brief | jq

demo-clients: check-api
	@echo "📊 Listing All Clients..."
	@echo ""
	@curl -s $(API_URL)/clients/list | jq

demo-client: check-api
	@echo "🏢 GreenTech Client Details..."
	@echo ""
	@curl -s $(API_URL)/clients/GreenTech | jq

demo-comms: check-api
	@echo "💬 Searching GreenTech Communications..."
	@echo ""
	@curl -s "$(API_URL)/clients/GreenTech/communications" | jq

demo-actions: check-api
	@echo "✅ GreenTech Action Items..."
	@echo ""
	@curl -s $(API_URL)/clients/GreenTech/action-items | jq

demo-kb: check-api
	@echo "🧠 Asking Knowledge Base about ESG Audits..."
	@echo ""
	@curl -s -X POST $(API_URL)/knowledge/ask \
		-H "Content-Type: application/json" \
		-d '{"question": "What are the key requirements for ESG audits?", "top_k": 3}' | jq

demo-topics: check-api
	@echo "📚 Knowledge Base Topics..."
	@echo ""
	@curl -s $(API_URL)/knowledge/topics | jq

demo-docs: check-api
	@echo "📄 Document Summaries..."
	@echo ""
	@curl -s $(API_URL)/documents/summaries | jq

#############################################
# API Examples (Raw)
#############################################

ex-list: check-api
	@curl -s $(API_URL)/clients/list | jq

ex-client: check-api
	@curl -s $(API_URL)/clients/GreenTech | jq

ex-brief: check-api
	@curl -s -X POST $(API_URL)/clients/GreenTech/meeting-brief | jq

ex-search: check-api
	@curl -s "$(API_URL)/clients/GreenTech/communications?query=ESG" | jq

ex-actions: check-api
	@curl -s $(API_URL)/clients/GreenTech/action-items | jq

ex-kb-ask: check-api
	@curl -s -X POST $(API_URL)/knowledge/ask \
		-H "Content-Type: application/json" \
		-d '{"question": "How do I prepare for an ESG audit?", "top_k": 3}' | jq

ex-kb-search: check-api
	@curl -s -X POST "$(API_URL)/knowledge/search?query=AI%20compliance&top_k=3" | jq

ex-kb-topics: check-api
	@curl -s $(API_URL)/knowledge/topics | jq

ex-docs-list: check-api
	@curl -s $(API_URL)/documents/list | jq

ex-docs-sum: check-api
	@curl -s $(API_URL)/documents/summaries | jq

#############################################
# Utilities
#############################################

health:
	@echo "🏥 Checking API Health..."
	@curl -s $(API_URL)/health | jq || echo "❌ API is not running"

clean:
	@echo "🧹 Cleaning cache files..."
	@rm -f data/knowledge_embeddings.json
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cache cleaned!"

logs:
	@echo "📋 Recent logs (last 50 lines)..."
	@tail -f -n 50 *.log 2>/dev/null || echo "No log files found"

#############################################
# Advanced Examples
#############################################

# Custom client query
ex-client-custom:
	@read -p "Enter client name: " client; \
	curl -s $(API_URL)/clients/$$client | jq

# Custom knowledge question
ex-kb-custom:
	@read -p "Enter your question: " question; \
	curl -s -X POST $(API_URL)/knowledge/ask \
		-H "Content-Type: application/json" \
		-d "{\"question\": \"$$question\", \"top_k\": 3}" | jq

# Save brief to file
save-brief:
	@mkdir -p output
	@curl -s -X POST $(API_URL)/clients/GreenTech/meeting-brief | jq > output/greentech-brief.json
	@echo "✅ Brief saved to output/greentech-brief.json"

# Quick test all endpoints
test-all: check-api
	@echo "🧪 Testing all endpoints..."
	@echo "1. Health..." && curl -s $(API_URL)/health > /dev/null && echo "  ✅" || echo "  ❌"
	@echo "2. Clients list..." && curl -s $(API_URL)/clients/list > /dev/null && echo "  ✅" || echo "  ❌"
	@echo "3. Client details..." && curl -s $(API_URL)/clients/GreenTech > /dev/null && echo "  ✅" || echo "  ❌"
	@echo "4. Meeting brief..." && curl -s -X POST $(API_URL)/clients/GreenTech/meeting-brief > /dev/null && echo "  ✅" || echo "  ❌"
	@echo "5. Knowledge topics..." && curl -s $(API_URL)/knowledge/topics > /dev/null && echo "  ✅" || echo "  ❌"
	@echo "6. Documents list..." && curl -s $(API_URL)/documents/list > /dev/null && echo "  ✅" || echo "  ❌"
	@echo "✅ All endpoints tested!"

#############################################
# Development
#############################################

dev:
	@echo "🔧 Starting development server with auto-reload..."
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 30903 --log-level debug

format:
	@echo "🎨 Formatting code..."
	@uv run black app/ || echo "black not installed, skipping..."
	@uv run isort app/ || echo "isort not installed, skipping..."

lint:
	@echo "🔍 Linting code..."
	@uv run ruff app/ || echo "ruff not installed, skipping..."

#############################################
# Docker
#############################################

docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t meeting-prep-assistant:latest .
	@echo "✅ Docker image built!"

docker-run:
	@echo "🐳 Starting with Docker Compose (local build)..."
	@if [ ! -f .env ]; then \
		echo "⚠️  .env file not found. Creating from template..."; \
		cp .env.example .env; \
		echo "📝 Please edit .env and add your OPENAI_API_KEY"; \
		exit 1; \
	fi
	docker compose up -d
	@echo "✅ API running at http://localhost:30903"
	@echo "📚 API Docs at http://localhost:30903/docs"
	@echo ""
	@echo "View logs: make docker-logs"
	@echo "Stop: make docker-stop"

docker-run-ghcr:
	@echo "🐳 Starting with pre-built image from GitHub Container Registry..."
	@if [ ! -f .env ]; then \
		echo "⚠️  .env file not found. Creating from template..."; \
		cp .env.example .env; \
		echo "📝 Please edit .env and add your OPENAI_API_KEY"; \
		exit 1; \
	fi
	@if ! grep -q "^GITHUB_REPOSITORY=" .env; then \
		echo "⚠️  GITHUB_REPOSITORY not set in .env"; \
		echo "📝 Add: GITHUB_REPOSITORY=your-username/meeting-prep-backend"; \
		exit 1; \
	fi
	docker compose -f docker-compose.ghcr.yml up -d
	@echo "✅ API running at http://localhost:30903"
	@echo "📚 API Docs at http://localhost:30903/docs"
	@echo ""
	@echo "View logs: make docker-logs-ghcr"
	@echo "Stop: make docker-stop-ghcr"

docker-pull:
	@echo "📥 Pulling latest image from GitHub Container Registry..."
	@if ! grep -q "^GITHUB_REPOSITORY=" .env 2>/dev/null; then \
		echo "⚠️  GITHUB_REPOSITORY not set in .env"; \
		echo "📝 Add: GITHUB_REPOSITORY=your-username/meeting-prep-backend"; \
		exit 1; \
	fi
	@. .env && docker pull ghcr.io/$${GITHUB_REPOSITORY}:$${IMAGE_TAG:-latest}
	@echo "✅ Image pulled!"

docker-stop:
	@echo "🛑 Stopping Docker containers..."
	docker compose down
	@echo "✅ Containers stopped!"

docker-stop-ghcr:
	@echo "🛑 Stopping Docker containers (GHCR)..."
	docker compose -f docker-compose.ghcr.yml down
	@echo "✅ Containers stopped!"

docker-logs:
	@echo "📋 Viewing Docker logs (Ctrl+C to exit)..."
	docker compose logs -f

docker-logs-ghcr:
	@echo "📋 Viewing Docker logs (GHCR) (Ctrl+C to exit)..."
	docker compose -f docker-compose.ghcr.yml logs -f

docker-shell:
	@echo "🐚 Opening shell in container..."
	docker compose exec api /bin/bash || docker compose exec api /bin/sh

docker-restart:
	@echo "🔄 Restarting Docker containers..."
	docker compose restart
	@echo "✅ Containers restarted!"

docker-clean:
	@echo "🧹 Cleaning Docker resources..."
	docker compose down -v
	docker rmi meeting-prep-assistant:latest || true
	@echo "✅ Docker resources cleaned!"

docker-rebuild:
	@echo "🔨 Rebuilding and restarting..."
	docker compose down
	docker build -t meeting-prep-assistant:latest .
	docker compose up -d
	@echo "✅ Rebuild complete!"

# Docker development mode (with volume mounts)
docker-dev:
	@echo "🔧 Starting in development mode..."
	docker compose -f docker compose.yml -f docker compose.dev.yml up

# Run examples against Docker container
docker-demo: 
	@echo "🎬 Running demo against Docker container..."
	@sleep 2  # Wait for container to be ready
	@make demo

docker-test:
	@echo "🧪 Testing Docker deployment..."
	@echo "Waiting for container to be ready..."
	@sleep 5
	@make health || (echo "❌ Health check failed" && exit 1)
	@echo "✅ Docker deployment is healthy!"
