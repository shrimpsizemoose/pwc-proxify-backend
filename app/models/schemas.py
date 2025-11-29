"""Pydantic schemas for API requests/responses"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class Contact(BaseModel):
    """Contact information"""
    id: str
    name: str
    role: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class Opportunity(BaseModel):
    """Sales opportunity"""
    id: str
    name: str
    stage: str
    amount: Optional[float] = None
    probability: Optional[float] = None
    close_date: Optional[str] = None


class Activity(BaseModel):
    """Client activity (call, meeting, email)"""
    id: str
    type: str
    subject: Optional[str] = None
    date: Optional[str] = None
    summary: Optional[str] = None


class ClientInfo(BaseModel):
    """Complete client information"""
    account_id: str
    name: str
    industry: Optional[str] = None
    region: Optional[str] = None
    esg_status: Optional[str] = None
    contacts: List[Contact] = []
    opportunities: List[Opportunity] = []
    activities: List[Activity] = []


class NewsItem(BaseModel):
    """News or regulatory item"""
    title: str
    summary: str
    date: Optional[str] = None
    source: Optional[str] = None
    relevance_score: Optional[float] = None


class MeetingBrief(BaseModel):
    """Generated meeting preparation brief"""
    client_name: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    # Client context
    client_overview: str
    key_contacts: List[Dict[str, Any]] = []

    # Opportunities & activities
    open_opportunities: List[Dict[str, Any]] = []
    recent_activities: List[Dict[str, Any]] = []

    # Intelligence
    recent_news: List[NewsItem] = []
    regulatory_alerts: List[NewsItem] = []

    # AI-generated insights
    talking_points: List[str] = []
    action_items: List[str] = []
    risks: List[str] = []

    # Full AI summary
    executive_summary: str


class KnowledgeQuery(BaseModel):
    """Knowledge base query"""
    question: str
    top_k: int = Field(default=3, ge=1, le=10)


class KnowledgeResponse(BaseModel):
    """Knowledge base answer"""
    question: str
    answer: str
    sources: List[str] = []
    confidence: Optional[float] = None
