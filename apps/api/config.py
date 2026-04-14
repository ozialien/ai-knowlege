from pydantic import BaseModel
import os

def _as_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}

class Settings(BaseModel):
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_chat_model: str = os.getenv("OLLAMA_CHAT_MODEL", "qwen3.5:9b")
    ollama_embed_model: str = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    ollama_rerank_model: str = os.getenv("OLLAMA_RERANK_MODEL", "")
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "docs")
    mlflow_tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    app_env: str = os.getenv("APP_ENV", "dev")
    max_chunk_size: int = int(os.getenv("MAX_CHUNK_SIZE", "900"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    retrieval_default_top_k: int = int(os.getenv("RETRIEVAL_DEFAULT_TOP_K", "5"))
    enable_rerank: bool = _as_bool(os.getenv("ENABLE_RERANK"), False)

settings = Settings()
