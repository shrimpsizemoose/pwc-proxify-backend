"""Knowledge base endpoints"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.services.knowledge_service import KnowledgeService
from app.services.ai_service import AIService
from app.utils.data_loader import DataLoader
from app.models.schemas import KnowledgeQuery, KnowledgeResponse

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


def get_knowledge_service() -> KnowledgeService:
    """Dependency: Get knowledge service instance"""
    data_loader = DataLoader()
    ai_service = AIService()
    return KnowledgeService(data_loader, ai_service)


@router.get("/topics")
async def list_topics(service: KnowledgeService = Depends(get_knowledge_service)) -> List[Dict[str, str]]:
    """List all available knowledge topics"""
    return service.get_all_topics()


@router.get("/topics/{topic_name}")
async def get_topic(
    topic_name: str,
    service: KnowledgeService = Depends(get_knowledge_service)
) -> Dict[str, str]:
    """Get full content for a specific topic"""
    content = service.get_topic_content(topic_name)

    if not content:
        raise HTTPException(status_code=404, detail=f"Topic '{topic_name}' not found")

    return {
        "topic": topic_name,
        "content": content,
    }


@router.post("/ask")
async def ask_question(
    query: KnowledgeQuery,
    service: KnowledgeService = Depends(get_knowledge_service)
) -> KnowledgeResponse:
    """Ask a question to the knowledge base (RAG)"""
    try:
        response = service.answer_question(query.question, top_k=query.top_k)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")


@router.post("/search")
async def search_knowledge(
    query: str,
    top_k: int = 3,
    service: KnowledgeService = Depends(get_knowledge_service)
) -> List[Dict[str, Any]]:
    """Search knowledge base semantically"""
    try:
        results = service.search_knowledge_base(query, top_k=top_k)

        return [
            {
                "title": doc["title"],
                "file": doc["file"],
                "similarity": float(similarity),
                "preview": doc["content"][:300] + "...",
            }
            for doc, similarity in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching knowledge base: {str(e)}")
