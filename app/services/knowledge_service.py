"""Knowledge base RAG service"""
from typing import List, Dict, Any, Tuple
import json
from pathlib import Path
from app.utils.data_loader import DataLoader
from app.services.ai_service import AIService
from app.models.schemas import KnowledgeResponse


class KnowledgeService:
    """RAG-based knowledge base Q&A"""

    def __init__(self, data_loader: DataLoader, ai_service: AIService):
        self.data_loader = data_loader
        self.ai_service = ai_service
        self._embeddings_cache: Dict[str, List[float]] = {}
        self._init_knowledge_base()

    def _init_knowledge_base(self):
        """Initialize knowledge base with embeddings"""
        # Load knowledge documents
        self.knowledge_docs = self.data_loader.load_knowledge_hub()

        # Check if embeddings are cached
        cache_file = Path("data/knowledge_embeddings.json")

        if cache_file.exists():
            try:
                with open(cache_file, "r") as f:
                    self._embeddings_cache = json.load(f)
                print(f"Loaded {len(self._embeddings_cache)} cached embeddings")
            except Exception as e:
                print(f"Error loading embeddings cache: {e}")
                self._compute_embeddings()
        else:
            self._compute_embeddings()

    def _compute_embeddings(self):
        """Compute and cache embeddings for knowledge base"""
        print("Computing embeddings for knowledge base...")

        for doc in self.knowledge_docs:
            doc_id = doc["file"]
            content = doc["content"]

            # Get embedding
            embedding = self.ai_service.get_embedding(content)

            if embedding:
                self._embeddings_cache[doc_id] = embedding

        # Save to cache
        cache_file = Path("data/knowledge_embeddings.json")
        cache_file.parent.mkdir(exist_ok=True)

        try:
            with open(cache_file, "w") as f:
                json.dump(self._embeddings_cache, f)
            print(f"Cached {len(self._embeddings_cache)} embeddings")
        except Exception as e:
            print(f"Error saving embeddings cache: {e}")

    def search_knowledge_base(self, query: str, top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        """Search knowledge base using semantic similarity"""
        # Get query embedding
        query_embedding = self.ai_service.get_embedding(query)

        if not query_embedding:
            return []

        # Calculate similarities
        results = []

        for doc in self.knowledge_docs:
            doc_id = doc["file"]

            if doc_id not in self._embeddings_cache:
                continue

            doc_embedding = self._embeddings_cache[doc_id]
            similarity = self.ai_service.cosine_similarity(query_embedding, doc_embedding)

            results.append((doc, similarity))

        # Sort by similarity and return top_k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def answer_question(self, question: str, top_k: int = 3) -> KnowledgeResponse:
        """Answer a question using RAG"""
        # Search knowledge base
        relevant_docs = self.search_knowledge_base(question, top_k=top_k)

        if not relevant_docs:
            return KnowledgeResponse(
                question=question,
                answer="I don't have any relevant information to answer that question.",
                sources=[],
                confidence=0.0,
            )

        # Build context from top documents
        context_parts = []
        sources = []

        for doc, similarity in relevant_docs:
            context_parts.append(f"### {doc['title']}\n{doc['content']}\n")
            sources.append(f"{doc['title']} (similarity: {similarity:.2f})")

        context = "\n\n".join(context_parts)

        # Generate answer using AI
        answer = self.ai_service.answer_with_context(question, context)

        # Calculate confidence based on top similarity score
        confidence = relevant_docs[0][1] if relevant_docs else 0.0

        return KnowledgeResponse(
            question=question,
            answer=answer,
            sources=sources,
            confidence=confidence,
        )

    def get_all_topics(self) -> List[Dict[str, str]]:
        """Get all available knowledge topics"""
        return [
            {
                "title": doc["title"],
                "file": doc["file"],
                "preview": doc["content"][:200] + "..."
            }
            for doc in self.knowledge_docs
        ]

    def get_topic_content(self, topic_name: str) -> str:
        """Get full content for a specific topic"""
        for doc in self.knowledge_docs:
            if topic_name.lower() in doc["title"].lower() or topic_name.lower() in doc["file"].lower():
                return doc["content"]

        return None
