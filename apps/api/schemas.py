from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    system: Optional[str] = "You are a concise local AI assistant."

class ChatResponse(BaseModel):
    response: str

class EmbedRequest(BaseModel):
    texts: List[str]

class EmbedResponse(BaseModel):
    embeddings_count: int

class IngestRequest(BaseModel):
    texts: List[str]
    source: Optional[str] = "manual"

class RAGRequest(BaseModel):
    question: str
    top_k: int = 4

class RAGResponse(BaseModel):
    answer: str
    contexts: List[str]

class AgentRequest(BaseModel):
    task: str
