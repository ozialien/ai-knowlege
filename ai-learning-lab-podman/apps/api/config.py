from pydantic import BaseModel
import os

class Settings(BaseModel):
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_chat_model: str = os.getenv("OLLAMA_CHAT_MODEL", "qwen3.5:9b")
    ollama_embed_model: str = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    qdrant_url: str = os.getenv("QDRANT_URL", "http://qdrant:6333")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "docs")
    mlflow_tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
    app_env: str = os.getenv("APP_ENV", "dev")
    max_chunk_size: int = int(os.getenv("MAX_CHUNK_SIZE", "900"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    langgraph_thread_id: str = os.getenv("LANGGRAPH_THREAD_ID", "lesson-thread")

settings = Settings()
