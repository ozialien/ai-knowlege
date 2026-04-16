from pydantic import BaseModel, Field
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

class PathIngestRequest(BaseModel):
    path: str = Field(..., description="Directory or file path accessible inside the API container")
    source: Optional[str] = "path"

class Citation(BaseModel):
    title: str = ""
    path: str = ""
    chunk_index: int = -1
    source: str = ""

class RAGRequest(BaseModel):
    question: str
    top_k: int = 5

class RAGResponse(BaseModel):
    answer: str
    contexts: List[str]
    citations: List[Citation]

class AgentRequest(BaseModel):
    task: str
    thread_id: Optional[str] = None
