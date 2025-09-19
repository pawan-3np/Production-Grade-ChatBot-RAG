import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = None
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "rag_agent"
    EBEDDING_MODEL: str = "gemini-embedding-001"
    EBEDDING_MODEL: int = 1536
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    TOP_K: int = 5
    LLM_MODEL: str = "gemini-generate-model-name"

    class Config:
        env_file = ".env"

settings = Settings()
    


