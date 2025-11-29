"""OpenAI integration service"""
from typing import List, Dict, Any
import numpy as np
from openai import OpenAI
from app.config import get_settings


class AIService:
    """Handle all AI/LLM operations"""

    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.embedding_model = settings.openai_embedding_model

    def get_embedding(self, text: str) -> List[float]:
        """Get embeddings for text"""
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return []

    def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple texts"""
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.embedding_model
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            print(f"Error getting batch embeddings: {e}")
            return []

    def cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        a_arr = np.array(a)
        b_arr = np.array(b)
        return float(np.dot(a_arr, b_arr) / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr)))

    def generate_completion(
        self,
        prompt: str,
        system_message: str = "You are a helpful assistant.",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate a completion using GPT"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating completion: {e}")
            return f"Error: {str(e)}"

    def generate_meeting_brief(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive meeting brief"""
        prompt = f"""
Generate a comprehensive meeting preparation brief for a consultant meeting with {client_data.get('account', {}).get('Name', 'Unknown Client')}.

CLIENT DATA:
{self._format_client_data(client_data)}

Please provide:
1. Executive Summary (2-3 sentences)
2. Client Overview (industry, region, key facts)
3. Key Contacts (who they are, their roles)
4. Open Opportunities (what's in the pipeline)
5. Recent Activities (last interactions)
6. Talking Points (5-7 specific topics to discuss)
7. Action Items (things to follow up on)
8. Potential Risks or Concerns

Format the response as JSON with these keys:
- executive_summary
- client_overview
- key_contacts_summary
- opportunities_summary
- talking_points (list)
- action_items (list)
- risks (list)
"""

        system_message = """You are a senior consultant assistant helping prepare for client meetings.
Be concise, actionable, and focus on business value. Format your response as valid JSON."""

        response = self.generate_completion(
            prompt=prompt,
            system_message=system_message,
            temperature=0.5,
            max_tokens=1500,
        )

        # Try to parse as JSON, fallback to structured text
        try:
            import json
            # Extract JSON from response (might be wrapped in markdown)
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response

            return json.loads(json_str)
        except:
            # Fallback: return as single summary
            return {
                "executive_summary": response,
                "client_overview": "",
                "key_contacts_summary": "",
                "opportunities_summary": "",
                "talking_points": [],
                "action_items": [],
                "risks": [],
            }

    def _format_client_data(self, client_data: Dict[str, Any]) -> str:
        """Format client data for prompt"""
        import json
        # Simplify complex data for better token usage
        formatted = {
            "account": client_data.get("account", {}),
            "contacts": client_data.get("contacts", [])[:5],  # Limit to 5
            "opportunities": client_data.get("opportunities", [])[:5],
            "activities": client_data.get("activities", [])[:10],
        }
        return json.dumps(formatted, indent=2, default=str)

    def summarize_document(self, content: str, doc_type: str = "document") -> str:
        """Summarize a document"""
        prompt = f"""Summarize this {doc_type} in 3-5 bullet points. Focus on key takeaways and action items.

CONTENT:
{content[:3000]}  # Limit content size
"""

        return self.generate_completion(
            prompt=prompt,
            system_message="You are a document summarization assistant. Be concise and actionable.",
            temperature=0.3,
            max_tokens=300,
        )

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract key entities from text"""
        prompt = f"""Extract key entities from this text and categorize them.

TEXT:
{text[:2000]}

Return as JSON with these categories:
- people (names of people)
- companies (company names)
- dates (important dates)
- topics (key topics/themes)
- action_items (things to do)
"""

        response = self.generate_completion(
            prompt=prompt,
            system_message="Extract entities and return valid JSON only.",
            temperature=0.2,
            max_tokens=500,
        )

        try:
            import json
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response
            return json.loads(json_str)
        except:
            return {
                "people": [],
                "companies": [],
                "dates": [],
                "topics": [],
                "action_items": [],
            }

    def answer_with_context(self, question: str, context: str) -> str:
        """Answer a question using provided context (RAG)"""
        prompt = f"""Answer the following question based ONLY on the provided context.
If the answer cannot be found in the context, say "I don't have enough information to answer that."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:"""

        return self.generate_completion(
            prompt=prompt,
            system_message="You are a knowledgeable assistant. Only use information from the provided context.",
            temperature=0.3,
            max_tokens=500,
        )
