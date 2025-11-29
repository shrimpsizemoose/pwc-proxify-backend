"""Meeting Prep Assistant API - Main Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routers import clients, knowledge, documents

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="""
    Backend API for Meeting Prep Assistant - helping consultants prepare for client meetings.

    ## Features

    * **Client Intelligence**: Aggregate data from CRM, emails, Teams, documents
    * **Meeting Briefs**: AI-generated comprehensive meeting preparation
    * **Knowledge Base**: RAG-powered Q&A over ESG, compliance, and regulatory docs
    * **Document Summarization**: AI summaries of proposals, agendas, action items
    * **Communication Search**: Find relevant emails and Teams discussions

    ## Data Sources

    - Salesforce CRM (Accounts, Contacts, Opportunities, Activities)
    - Email (.eml files)
    - Teams Chats (JSON)
    - SharePoint Documents (docx, xlsx, pptx)
    - News Feed (external signals)
    - Regulatory Feed (compliance alerts)
    - Knowledge Hub (ESG audits, AI Act compliance)
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(clients.router)
app.include_router(knowledge.router)
app.include_router(documents.router)


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "app": settings.app_name,
        "version": settings.version,
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "clients": "/clients",
            "knowledge": "/knowledge",
            "documents": "/documents",
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port, reload=settings.debug)
