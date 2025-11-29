# Meeting Prep Assistant API

Backend API for helping consultants prepare for client meetings by aggregating intelligence from multiple data sources.

## Features

- **Client Intelligence**: Aggregate CRM, emails, Teams chats, documents
- **AI Meeting Briefs**: GPT-powered comprehensive meeting preparation
- **Knowledge Base Q&A**: RAG over ESG/compliance documentation
- **Document Summarization**: AI summaries of proposals, agendas, presentations
- **Communication Search**: Find relevant emails and Teams discussions
- **Action Item Extraction**: Automatically extract tasks from various sources

## Tech Stack

- **Framework**: FastAPI
- **AI**: OpenAI GPT-4o-mini + text-embedding-3-small
- **Data Processing**: Pandas, python-docx, openpyxl, python-pptx
- **Package Manager**: uv

## Quick Start

### Option 1: Using Docker (Recommended for Quick Demo)

```bash
# 1. Setup
make setup
nano .env  # Add OPENAI_API_KEY

# 2. Build and run
make docker-build
make docker-run

# 3. Access
# API: http://localhost:8000
# Docs: http://localhost:8000/docs

# 4. Test
make demo
```

See [DOCKER.md](DOCKER.md) for detailed Docker instructions.

### Option 2: Using uv (For Development)

```bash
# 1. Setup
cd meeting-prep-backend
cp .env.example .env
nano .env  # Add your OpenAI API key

# 2. Install Dependencies
uv sync

# 3. Run the API
uv run uvicorn app.main:app --reload

# Or directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access API Documentation

Open your browser:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Client Intelligence

```http
GET /clients/list
# List all clients

GET /clients/{client_name}
# Get detailed client info

POST /clients/{client_name}/meeting-brief
# Generate AI meeting brief

GET /clients/{client_name}/communications?query=ESG
# Search emails and Teams chats

GET /clients/{client_name}/action-items
# Extract action items
```

### Knowledge Base

```http
GET /knowledge/topics
# List all knowledge topics

POST /knowledge/ask
# Ask a question (RAG)
Body: {"question": "What are ESG audit requirements?", "top_k": 3}

POST /knowledge/search?query=AI%20compliance&top_k=3
# Semantic search
```

### Documents

```http
GET /documents/list
# List all documents

GET /documents/summaries?doc_type=all
# Get AI summaries of documents
```

## Example Usage

### Generate Meeting Brief

```bash
curl -X POST "http://localhost:8000/clients/GreenTech%20Solutions/meeting-brief"
```

Response:
```json
{
  "client_name": "GreenTech Solutions",
  "generated_at": "2025-11-29T10:30:00",
  "client_overview": "Technology company focused on sustainability...",
  "key_contacts": [
    {"name": "John Doe", "role": "CFO", "email": "john@greentech.com"}
  ],
  "open_opportunities": [
    {"name": "ESG Audit 2025", "stage": "Proposal", "amount": 2000000}
  ],
  "talking_points": [
    "Congratulate on recent TechCrunch feature",
    "Discuss EU AI Act compliance timeline",
    "Review ESG audit scope and timeline"
  ],
  "executive_summary": "GreenTech Solutions is a high-value client..."
}
```

### Ask Knowledge Base

```bash
curl -X POST "http://localhost:8000/knowledge/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the key steps for ESG audits?", "top_k": 3}'
```

Response:
```json
{
  "question": "What are the key steps for ESG audits?",
  "answer": "Based on the ESG audit preparation guide, the key steps are...",
  "sources": [
    "Preparing for ESG Audits (similarity: 0.89)",
    "AI Act Compliance Overview (similarity: 0.45)"
  ],
  "confidence": 0.89
}
```

## Project Structure

```
meeting-prep-backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models/              # Pydantic schemas
│   │   └── schemas.py
│   ├── routers/             # API endpoints
│   │   ├── clients.py       # Client intelligence
│   │   ├── knowledge.py     # Knowledge base
│   │   └── documents.py     # Document processing
│   ├── services/            # Business logic
│   │   ├── ai_service.py           # OpenAI integration
│   │   ├── intelligence_service.py # Client intelligence
│   │   └── knowledge_service.py    # RAG knowledge base
│   └── utils/               # Utilities
│       └── data_loader.py   # Data parsing
├── data/                    # Cache directory
├── .env                     # Environment variables
├── .env.example            # Environment template
├── pyproject.toml          # uv configuration
└── README.md               # This file
```

## Data Sources

The API expects data in the parent directory:

```
../
├── hackathon_fake_salesforce/
│   ├── Accounts.csv
│   ├── Contacts.csv
│   ├── Opportunities.csv
│   └── Activities.csv
├── hackathon_fake_mail_teams/
│   ├── mail/*.eml
│   └── teams/*.json
├── hackathon_fake_sharepoint_news/
│   ├── sharepoint/*.docx,*.xlsx,*.pptx
│   └── news_feed/NewsFeed.json
└── hackathon_extra_calendar_knowledge_regulatory/
    ├── knowledge_hub/*.md
    └── regulatory_feed/RegulatoryFeed.json
```

## Development

### Add Dependencies

```bash
uv add package-name
```

### Run Tests

```bash
# TODO: Add tests
uv run pytest
```

### Format Code

```bash
uv run black app/
uv run isort app/
```

## Configuration

Edit `.env` file:

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional (defaults provided)
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
DEBUG=True
```

## Performance Notes

- **Embeddings Caching**: Knowledge base embeddings are cached in `data/knowledge_embeddings.json`
- **Data Caching**: Parsed data is cached in memory during runtime
- **Token Usage**: Uses gpt-4o-mini for cost efficiency while maintaining quality

## Hackathon Tips

1. **Demo Flow**:
   - Show client list: `GET /clients/list`
   - Pick a client: `GET /clients/GreenTech`
   - Generate brief: `POST /clients/GreenTech/meeting-brief`
   - Ask knowledge: `POST /knowledge/ask`

2. **Key Selling Points**:
   - Parses 7+ data formats automatically
   - AI-powered insights and summarization
   - Semantic search over knowledge base
   - Real-time meeting prep in seconds

3. **Future Enhancements** (mention during judging):
   - Real-time data connectors (live Salesforce, Outlook)
   - Mobile app integration
   - Slack/Teams bot interface
   - Custom knowledge base uploads
   - Multi-language support

## License

MIT (Hackathon Project)
