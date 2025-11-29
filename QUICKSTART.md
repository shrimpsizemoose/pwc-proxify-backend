# Quick Start Guide - 5 Minutes to Demo

## Prerequisites

- Python 3.11+
- OpenAI API key
- Data files in parent directory (already extracted)

## Setup (2 minutes)

```bash
cd meeting-prep-backend

# 1. Install dependencies
uv sync

# 2. Configure environment
cp .env.example .env
nano .env  # Add your OPENAI_API_KEY

# 3. Verify setup
uv run python test_setup.py
```

## Run (1 minute)

```bash
# Start the API
./run.sh

# Or manually
uv run uvicorn app.main:app --reload
```

Server starts at: http://localhost:8000

## Test (2 minutes)

### Option 1: Interactive Docs (Recommended)

1. Open: http://localhost:8000/docs
2. Try "POST /clients/{client_name}/meeting-brief"
3. Enter: `GreenTech`
4. Click "Execute"

### Option 2: Command Line

```bash
# Generate meeting brief
curl -X POST http://localhost:8000/clients/GreenTech/meeting-brief | jq

# Ask knowledge base
curl -X POST http://localhost:8000/knowledge/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are ESG audit requirements?"}' | jq
```

## Key Endpoints for Demo

```
POST /clients/{name}/meeting-brief  ← Main feature!
POST /knowledge/ask                  ← RAG Q&A
GET  /clients/list                   ← Show all clients
GET  /documents/summaries            ← AI doc summaries
```

## Common Issues

**"Client not found"**: Use `GreenTech` (check case)

**OpenAI errors**: Verify API key in `.env`

**Import errors**: Run `uv sync`

**Data not loading**: Run from `meeting-prep-backend/` directory

## For Your Team

### Frontend Integration

```javascript
// Base URL
const API_URL = 'http://localhost:8000';

// Generate meeting brief
const brief = await fetch(
  `${API_URL}/clients/GreenTech/meeting-brief`,
  { method: 'POST' }
).then(r => r.json());

console.log(brief.talking_points);
console.log(brief.executive_summary);
```

### API Response Structure

```typescript
interface MeetingBrief {
  client_name: string;
  generated_at: string;
  client_overview: string;
  key_contacts: Contact[];
  open_opportunities: Opportunity[];
  recent_activities: Activity[];
  recent_news: NewsItem[];
  regulatory_alerts: NewsItem[];
  talking_points: string[];
  action_items: string[];
  risks: string[];
  executive_summary: string;
}
```

### CORS

Already configured to accept all origins for development.

## Architecture Overview

```
Frontend (Your Team)
    ↓ HTTP/REST
Backend API (FastAPI)
    ↓
├── Data Parsers → CSV, JSON, EML, DOCX, XLSX, PPTX
├── OpenAI Service → GPT-4o-mini + Embeddings
├── Intelligence Service → Aggregate client data
└── Knowledge Service → RAG over markdown docs
```

## Demo Script

**Scenario**: Consultant preparing for GreenTech meeting

1. **Show client list**: `GET /clients/list`
2. **Get client info**: `GET /clients/GreenTech`
3. **Generate brief**: `POST /clients/GreenTech/meeting-brief`
4. **Ask about ESG**: `POST /knowledge/ask` with "ESG audit steps"
5. **Show documents**: `GET /documents/summaries`

**Highlight**:
- Aggregates 7+ data formats
- AI-powered insights
- Semantic knowledge search
- Ready in seconds vs hours of manual prep

## Next Steps

- See `README.md` for full documentation
- See `API_EXAMPLES.md` for more examples
- Check `/docs` endpoint for interactive API docs

## Need Help?

Check the logs when running with `./run.sh` - errors will be visible there.
