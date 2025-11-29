"""Configuration settings"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    app_name: str = "Meeting Prep Assistant API"
    version: str = "0.1.0"
    debug: bool = True

    # OpenAI Settings
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    # Data paths (relative to project root)
    data_path: str = "../"
    salesforce_path: str = "../hackathon_fake_salesforce"
    sharepoint_path: str = "../hackathon_fake_sharepoint_news"
    calendar_path: str = "../hackathon_extra_calendar_knowledge_regulatory"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
