"""Client intelligence and meeting preparation service"""
from typing import Dict, Any, List
from datetime import datetime
from app.utils.data_loader import DataLoader
from app.services.ai_service import AIService
from app.models.schemas import MeetingBrief, NewsItem


class IntelligenceService:
    """Aggregate client intelligence from multiple sources"""

    def __init__(self, data_loader: DataLoader, ai_service: AIService):
        self.data_loader = data_loader
        self.ai_service = ai_service

    def get_client_info(self, client_name: str) -> Dict[str, Any]:
        """Get comprehensive client information"""
        client_data = self.data_loader.get_client_by_name(client_name)

        if not client_data:
            return None

        return client_data

    def generate_meeting_brief(self, client_name: str) -> MeetingBrief:
        """Generate comprehensive meeting preparation brief"""
        # Get client data
        client_data = self.get_client_info(client_name)

        if not client_data:
            raise ValueError(f"Client '{client_name}' not found")

        # Get news and regulatory data
        news_items = self._get_relevant_news(client_name)
        regulatory_items = self._get_relevant_regulatory(client_name)

        # Get AI-generated insights
        ai_brief = self.ai_service.generate_meeting_brief(client_data)

        # Build meeting brief
        account = client_data["account"]

        brief = MeetingBrief(
            client_name=account.get("Name", client_name),
            client_overview=ai_brief.get("client_overview", ""),
            key_contacts=[
                {
                    "name": c.get("Name", ""),
                    "role": c.get("Role", ""),
                    "email": c.get("Email", ""),
                }
                for c in client_data.get("contacts", [])[:5]
            ],
            open_opportunities=[
                {
                    "name": o.get("Name", ""),
                    "stage": o.get("Stage", ""),
                    "amount": o.get("Amount", 0),
                    "probability": o.get("Probability", 0),
                }
                for o in client_data.get("opportunities", [])
            ],
            recent_activities=[
                {
                    "type": a.get("Type", ""),
                    "subject": a.get("Subject", ""),
                    "date": str(a.get("ActivityDate", "")),
                }
                for a in client_data.get("activities", [])[:10]
            ],
            recent_news=news_items,
            regulatory_alerts=regulatory_items,
            talking_points=ai_brief.get("talking_points", []),
            action_items=ai_brief.get("action_items", []),
            risks=ai_brief.get("risks", []),
            executive_summary=ai_brief.get("executive_summary", ""),
        )

        return brief

    def _get_relevant_news(self, client_name: str) -> List[NewsItem]:
        """Get news relevant to the client"""
        news_feed = self.data_loader.load_news_feed()

        # Simple keyword matching (in hackathon, can be basic)
        relevant_news = []

        for item in news_feed:
            # Check if client name appears in title or summary
            title = item.get("title", "")
            summary = item.get("summary", "")

            if client_name.lower() in title.lower() or client_name.lower() in summary.lower():
                relevant_news.append(
                    NewsItem(
                        title=title,
                        summary=summary,
                        date=item.get("date", ""),
                        source=item.get("source", ""),
                        relevance_score=1.0,
                    )
                )

        return relevant_news[:5]  # Top 5

    def _get_relevant_regulatory(self, client_name: str = None) -> List[NewsItem]:
        """Get relevant regulatory updates"""
        regulatory_feed = self.data_loader.load_regulatory_feed()

        # Get recent regulatory items (all are relevant for consultants)
        regulatory_items = []

        for item in regulatory_feed[:5]:  # Top 5 recent
            regulatory_items.append(
                NewsItem(
                    title=item.get("title", ""),
                    summary=item.get("summary", ""),
                    date=item.get("deadline", item.get("date", "")),
                    source="Regulatory Feed",
                )
            )

        return regulatory_items

    def search_communications(self, client_name: str, query: str = None) -> Dict[str, Any]:
        """Search emails and Teams chats for a client"""
        emails = self.data_loader.load_emails()
        teams_chats = self.data_loader.load_teams_chats()

        results = {"emails": [], "teams": []}

        # Filter emails
        for email in emails:
            if client_name.lower() in email.get("subject", "").lower() or \
               client_name.lower() in email.get("body", "").lower():
                if query is None or query.lower() in email.get("body", "").lower():
                    results["emails"].append({
                        "subject": email.get("subject"),
                        "from": email.get("from"),
                        "date": email.get("date"),
                        "preview": email.get("body", "")[:200] + "..."
                    })

        # Filter Teams chats
        for chat in teams_chats:
            messages = chat.get("messages", [])
            relevant_messages = []

            for msg in messages:
                content = msg.get("content", "")
                if client_name.lower() in content.lower():
                    if query is None or query.lower() in content.lower():
                        relevant_messages.append(msg)

            if relevant_messages:
                results["teams"].append({
                    "thread": chat.get("thread_name", ""),
                    "messages": relevant_messages[:5]  # Limit messages
                })

        return results

    def get_document_summary(self, document_type: str = "all") -> List[Dict[str, Any]]:
        """Get summaries of SharePoint documents"""
        docs = self.data_loader.load_sharepoint_docs()
        summaries = []

        # Summarize DOCX
        if document_type in ["all", "docx"]:
            for doc in docs.get("docx", []):
                summary = self.ai_service.summarize_document(
                    doc["content"], doc_type="meeting agenda"
                )
                summaries.append({
                    "file": doc["file"],
                    "type": "docx",
                    "summary": summary,
                })

        # Summarize XLSX (action logs)
        if document_type in ["all", "xlsx"]:
            for doc in docs.get("xlsx", []):
                import json
                content = json.dumps(doc["data"], indent=2)
                summary = self.ai_service.summarize_document(
                    content, doc_type="action log"
                )
                summaries.append({
                    "file": doc["file"],
                    "type": "xlsx",
                    "summary": summary,
                    "data": doc["data"][:10],  # Include sample data
                })

        # Summarize PPTX
        if document_type in ["all", "pptx"]:
            for doc in docs.get("pptx", []):
                content = "\n\n".join(doc["slides"])
                summary = self.ai_service.summarize_document(
                    content, doc_type="presentation"
                )
                summaries.append({
                    "file": doc["file"],
                    "type": "pptx",
                    "summary": summary,
                    "slide_count": doc["slide_count"],
                })

        return summaries

    def extract_action_items(self, client_name: str = None) -> List[Dict[str, Any]]:
        """Extract action items from various sources"""
        action_items = []

        # From SharePoint action logs
        docs = self.data_loader.load_sharepoint_docs()
        for doc in docs.get("xlsx", []):
            if "action" in doc["file"].lower():
                for item in doc["data"]:
                    action_items.append({
                        "source": doc["file"],
                        "action": item.get("Action", ""),
                        "owner": item.get("Owner", ""),
                        "deadline": item.get("Deadline", ""),
                        "status": item.get("Status", ""),
                    })

        # From emails (AI extraction)
        emails = self.data_loader.load_emails()
        for email in emails[:5]:  # Limit for speed
            if client_name and client_name.lower() not in email.get("body", "").lower():
                continue

            entities = self.ai_service.extract_entities(email.get("body", ""))
            for action in entities.get("action_items", []):
                action_items.append({
                    "source": f"Email: {email.get('subject')}",
                    "action": action,
                    "owner": "TBD",
                    "deadline": "TBD",
                    "status": "Open",
                })

        return action_items
