from fastapi import FastAPI, HTTPException
from apps.api.schemas import (
    ChatRequest, ChatResponse, EmbedRequest, EmbedResponse,
    IngestRequest, PathIngestRequest, RAGRequest, RAGResponse, AgentRequest, Citation
)
from apps.api.ollama_client import chat, embed
from apps.api.config import settings
from apps.api.mlflow_utils import log_chat, log_rag, log_ingestion
from rag.ingest import prepare_texts, prepare_path
from rag.qdrant_store import upsert_texts
from rag.retrieval import retrieve_contexts, format_citations
from agents.simple_graph import build_graph

app = FastAPI(title="AI Platform V4 Podman", version="0.4.0")
graph = build_graph()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "env": settings.app_env,
        "chat_model": settings.ollama_chat_model,
        "embed_model": settings.ollama_embed_model,
        "rerank_enabled": settings.enable_rerank,
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

@app.post("/ingest/texts")
async def ingest_texts(req: IngestRequest):
    chunks = prepare_texts(req.texts)
    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks produced from input texts")
    vectors = await embed(chunks)
    count = upsert_texts(chunks, vectors, req.source or "manual")
    log_ingestion(req.source or "manual", count)
    return {"status": "ok", "chunks_indexed": count}

@app.post("/ingest/path")
async def ingest_path(req: PathIngestRequest):
    records = prepare_path(req.path)
    if not records:
        raise HTTPException(status_code=400, detail="No ingestible files or chunks found")
    texts = [r["text"] for r in records]
    payloads = [{k: v for k, v in r.items() if k != "text"} for r in records]
    vectors = await embed(texts)
    count = upsert_texts(texts, vectors, req.source or "path", payloads=payloads)
    log_ingestion(req.source or "path", count)
    return {"status": "ok", "chunks_indexed": count}

@app.post("/rag/answer", response_model=RAGResponse)
async def rag_answer(req: RAGRequest):
    contexts = await retrieve_contexts(req.question, top_k=req.top_k or settings.retrieval_default_top_k)
    context_texts = [c["text"] for c in contexts]
    prompt = (
        "Answer the question using the provided context. "
        "If the answer is not in context, say so. "
        "At the end, include a short 'Sources used' line.\n\n"
        f"Question: {req.question}\n\n"
        "Context:\n" + "\n---\n".join(context_texts)
    )
    answer = await chat(prompt, "You are a grounded RAG assistant.")
    citations = [Citation(**c) for c in format_citations(contexts)]
    log_rag(req.question, answer, req.top_k, len(context_texts))
    return RAGResponse(answer=answer, contexts=context_texts, citations=citations)

@app.post("/agent/run")
async def agent_run(req: AgentRequest):
    thread_id = req.thread_id or settings.langgraph_thread_id
    result = await graph.ainvoke(
        {"task": req.task, "plan": "", "answer": ""},
        config={"configurable": {"thread_id": thread_id}},
    )
    return {"thread_id": thread_id, **result}
