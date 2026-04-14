from pydantic import BaseModel
import os

class Settings(BaseModel):
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_chat_model: str = os.getenv("OLLAMA_CHAT_MODEL", "qwen3.5:9b")
    ollama_embed_model: str = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "docs")
    mlflow_tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    app_env: str = os.getenv("APP_ENV", "dev")

settings = Settings()
