from fastapi import FastAPI
from apps.api.schemas import (
    ChatRequest, ChatResponse, EmbedRequest, EmbedResponse,
    IngestRequest, RAGRequest, RAGResponse, AgentRequest
)
from apps.api.ollama_client import chat, embed
from apps.api.config import settings
from apps.api.mlflow_utils import log_chat, log_rag
from rag.ingest import prepare_texts
from rag.qdrant_store import upsert_texts, search
from agents.simple_graph import build_graph

app = FastAPI(title="AI Platform V2", version="0.2.0")
graph = build_graph()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "env": settings.app_env,
        "chat_model": settings.ollama_chat_model,
        "embed_model": settings.ollama_embed_model,
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    response = await chat(req.message, req.system)
    log_chat(req.message, response, settings.ollama_chat_model)
    return ChatResponse(response=response)

@app.post("/embed", response_model=EmbedResponse)
async def embed_endpoint(req: EmbedRequest):
    vectors = await embed(req.texts)
    return EmbedResponse(embeddings_count=len(vectors))

@app.post("/ingest")
async def ingest_endpoint(req: IngestRequest):
    chunks = prepare_texts(req.texts)
    vectors = await embed(chunks)
    count = upsert_texts(chunks, vectors, req.source or "manual")
    return {"status": "ok", "chunks_indexed": count}

@app.post("/rag/answer", response_model=RAGResponse)
async def rag_answer(req: RAGRequest):
    query_vector = (await embed([req.question]))[0]
    contexts = search(query_vector, top_k=req.top_k)
    prompt = (
        "Answer the question using the provided context. "
        "If the answer is not in context, say so.\n\n"
        f"Question: {req.question}\n\n"
        "Context:\n" + "\n---\n".join(contexts)
    )
    answer = await chat(prompt, "You are a grounded RAG assistant.")
    log_rag(req.question, answer, req.top_k)
    return RAGResponse(answer=answer, contexts=contexts)

@app.post("/agent/run")
async def agent_run(req: AgentRequest):
    result = await graph.ainvoke({"task": req.task, "plan": "", "answer": ""})
    return result
