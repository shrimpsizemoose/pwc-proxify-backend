"""Document processing endpoints"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.services.intelligence_service import IntelligenceService
from app.services.ai_service import AIService
from app.utils.data_loader import DataLoader

router = APIRouter(prefix="/documents", tags=["documents"])


def get_intelligence_service() -> IntelligenceService:
    """Dependency: Get intelligence service instance"""
    try:
        data_loader = DataLoader()
        ai_service = AIService()
        return IntelligenceService(data_loader, ai_service)
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Failed to initialize document service: {str(e)}")


@router.get("/summaries")
async def get_document_summaries(
    doc_type: str = "all",
    service: IntelligenceService = Depends(get_intelligence_service)
) -> List[Dict[str, Any]]:
    """Get AI-generated summaries of all documents"""
    try:
        summaries = service.get_document_summary(document_type=doc_type)
        return summaries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summaries: {str(e)}")


@router.get("/list")
async def list_documents(service: IntelligenceService = Depends(get_intelligence_service)) -> Dict[str, Any]:
    """List all available documents"""
    try:
        docs = service.data_loader.load_sharepoint_docs()

        return {
            "word_documents": [{"file": d["file"], "paragraphs": d["paragraphs"]} for d in docs.get("docx", [])],
            "excel_documents": [{"file": d["file"], "columns": d["columns"]} for d in docs.get("xlsx", [])],
            "powerpoint_documents": [{"file": d["file"], "slide_count": d["slide_count"]} for d in docs.get("pptx", [])],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")
