from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "AgentShield"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = "sqlite:///./agentshield.db"
    
    # Security
    SECRET_KEY: str = "generate-a-strong-secret-key-for-production"
    CORS_ORIGINS: list[str] = ["*"]
    
    # LLM Provider
    LLM_PROVIDER: str = "demo"
    LLM_MODEL: str = ""
    LLM_API_KEY: str = ""
    GROQ_API_KEY: str = ""

    class Config:
        env_file = "../.env"
        env_file_encoding = 'utf-8'
        extra = 'ignore'

@lru_cache()
def get_settings():
    return Settings()
