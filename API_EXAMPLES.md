# API Examples & Testing

Quick reference for testing the Meeting Prep Assistant API.

## Prerequisites

```bash
# Start the server
./run.sh

# Or manually
uv run uvicorn app.main:app --reload
```

Server runs at: http://localhost:8000

## 1. Client Intelligence

### List All Clients

```bash
curl http://localhost:8000/clients/list | jq
```

Expected response:
```json
[
  {
    "AccountId": "ACC001",
    "Name": "GreenTech Solutions",
    "Industry": "Technology",
    "Region": "EMEA",
    "ESGStatus": "Active"
  }
]
```

### Get Client Details

```bash
curl http://localhost:8000/clients/GreenTech | jq
```

### Generate Meeting Brief (Main Feature!)

```bash
curl -X POST http://localhost:8000/clients/GreenTech/meeting-brief | jq
```

Expected response:
```json
{
  "client_name": "GreenTech Solutions",
  "generated_at": "2025-11-29T10:30:00",
  "client_overview": "Technology company...",
  "key_contacts": [...],
  "open_opportunities": [...],
  "recent_activities": [...],
  "recent_news": [...],
  "regulatory_alerts": [...],
  "talking_points": [
    "Discuss Q4 strategy",
    "Review ESG audit timeline"
  ],
  "action_items": [
    "Send updated proposal",
    "Schedule follow-up call"
  ],
  "risks": [],
  "executive_summary": "Comprehensive summary..."
}
```

### Search Communications

```bash
# All communications for a client
curl http://localhost:8000/clients/GreenTech/communications | jq

# With search query
curl "http://localhost:8000/clients/GreenTech/communications?query=ESG" | jq
```

### Get Action Items

```bash
curl http://localhost:8000/clients/GreenTech/action-items | jq
```

## 2. Knowledge Base (RAG)

### List All Knowledge Topics

```bash
curl http://localhost:8000/knowledge/topics | jq
```

Expected response:
```json
[
  {
    "title": "Preparing for ESG Audits",
    "file": "Preparing_for_ESG_Audits.md",
    "preview": "# ESG Audit Preparation\n\n..."
  },
  {
    "title": "AI Act Compliance Overview",
    "file": "AI_Act_Compliance_Overview.md",
    "preview": "# EU AI Act Compliance\n\n..."
  }
]
```

### Ask a Question (RAG)

```bash
curl -X POST http://localhost:8000/knowledge/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the key requirements for ESG audits?",
    "top_k": 3
  }' | jq
```

Expected response:
```json
{
  "question": "What are the key requirements for ESG audits?",
  "answer": "Based on the ESG audit preparation guide, the key requirements include: 1) Environmental impact assessment...",
  "sources": [
    "Preparing for ESG Audits (similarity: 0.89)",
    "AI Act Compliance Overview (similarity: 0.34)"
  ],
  "confidence": 0.89
}
```

### Search Knowledge Base

```bash
curl -X POST "http://localhost:8000/knowledge/search?query=AI%20compliance&top_k=3" | jq
```

### Get Specific Topic

```bash
curl http://localhost:8000/knowledge/topics/ESG | jq
```

## 3. Documents

### List All Documents

```bash
curl http://localhost:8000/documents/list | jq
```

Expected response:
```json
{
  "word_documents": [
    {"file": "Meeting_Agenda.docx", "paragraphs": 15}
  ],
  "excel_documents": [
    {"file": "Action_Log.xlsx", "columns": ["Action", "Owner", "Deadline"]}
  ],
  "powerpoint_documents": [
    {"file": "Proposal_Deck.pptx", "slide_count": 12}
  ]
}
```

### Get Document Summaries

```bash
# All documents
curl http://localhost:8000/documents/summaries | jq

# Specific type
curl "http://localhost:8000/documents/summaries?doc_type=docx" | jq
```

Expected response:
```json
[
  {
    "file": "Meeting_Agenda.docx",
    "type": "docx",
    "summary": "- Quarterly review meeting\n- Budget discussion\n- Project timeline updates"
  },
  {
    "file": "Action_Log.xlsx",
    "type": "xlsx",
    "summary": "- 5 open action items\n- 3 assigned to John Doe\n- Next deadline: Dec 1, 2025",
    "data": [...]
  }
]
```

## 4. Health & Status

### Root Endpoint

```bash
curl http://localhost:8000/ | jq
```

### Health Check

```bash
curl http://localhost:8000/health | jq
```

## Python Examples

### Using `requests` library

```python
import requests

BASE_URL = "http://localhost:8000"

# List clients
response = requests.get(f"{BASE_URL}/clients/list")
clients = response.json()
print(f"Found {len(clients)} clients")

# Generate meeting brief
response = requests.post(f"{BASE_URL}/clients/GreenTech/meeting-brief")
brief = response.json()
print(f"Talking points: {brief['talking_points']}")

# Ask knowledge base
response = requests.post(
    f"{BASE_URL}/knowledge/ask",
    json={
        "question": "How do I prepare for an ESG audit?",
        "top_k": 3
    }
)
answer = response.json()
print(f"Answer: {answer['answer']}")
```

### Using `httpx` (async)

```python
import httpx
import asyncio

async def demo():
    async with httpx.AsyncClient() as client:
        # Get client info
        response = await client.get("http://localhost:8000/clients/GreenTech")
        client_data = response.json()

        # Generate brief
        response = await client.post(
            "http://localhost:8000/clients/GreenTech/meeting-brief"
        )
        brief = response.json()

        print(f"Executive Summary: {brief['executive_summary']}")

asyncio.run(demo())
```

## JavaScript Examples

### Using `fetch`

```javascript
// List clients
const response = await fetch('http://localhost:8000/clients/list');
const clients = await response.json();
console.log(`Found ${clients.length} clients`);

// Generate meeting brief
const briefResponse = await fetch(
  'http://localhost:8000/clients/GreenTech/meeting-brief',
  { method: 'POST' }
);
const brief = await briefResponse.json();
console.log('Talking points:', brief.talking_points);

// Ask knowledge base
const kbResponse = await fetch(
  'http://localhost:8000/knowledge/ask',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      question: "What are ESG audit requirements?",
      top_k: 3
    })
  }
);
const answer = await kbResponse.json();
console.log('Answer:', answer.answer);
```

### Using `axios`

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

// Get meeting brief
const brief = await axios.post(`${BASE_URL}/clients/GreenTech/meeting-brief`);
console.log(brief.data);

// Search knowledge
const knowledge = await axios.post(`${BASE_URL}/knowledge/ask`, {
  question: "How to comply with EU AI Act?",
  top_k: 3
});
console.log(knowledge.data.answer);
```

## Demo Flow for Hackathon

### Scenario: Preparing for GreenTech Meeting

```bash
# 1. Find the client
curl http://localhost:8000/clients/list | jq '.[] | select(.Name | contains("Green"))'

# 2. Get full client details
curl http://localhost:8000/clients/GreenTech | jq

# 3. Generate comprehensive meeting brief
curl -X POST http://localhost:8000/clients/GreenTech/meeting-brief | jq > brief.json

# 4. Review talking points
cat brief.json | jq '.talking_points'

# 5. Check action items
curl http://localhost:8000/clients/GreenTech/action-items | jq

# 6. Ask about ESG compliance (they have ESG opportunities)
curl -X POST http://localhost:8000/knowledge/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What should I know about ESG audits?"}' | jq '.answer'

# 7. Get document summaries
curl http://localhost:8000/documents/summaries | jq
```

## Testing Tips

1. **Use jq**: Install with `brew install jq` (Mac) or `apt install jq` (Linux)
2. **Pretty JSON**: Add `| jq` to any curl command
3. **Save responses**: Add `> output.json` to save
4. **Interactive Docs**: Visit http://localhost:8000/docs for Swagger UI

## Common Issues

### "Client not found"
- Check available clients: `curl http://localhost:8000/clients/list`
- Client names are case-sensitive
- Use URL encoding for spaces: `GreenTech%20Solutions`

### OpenAI API Errors
- Check `.env` has valid `OPENAI_API_KEY`
- Ensure you have credits in your OpenAI account
- Check rate limits

### Empty responses
- Ensure data files are in parent directory
- Check logs for parsing errors
- Run from `meeting-prep-backend/` directory
