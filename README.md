# AI Platform V2 Starter

A local AI engineering starter kit designed for:
- Ollama + Qwen 3.5
- FastAPI API layer
- Qdrant vector database
- MLflow experiment/eval logging
- LangGraph agent scaffolding
- Docker Compose local orchestration

## Included
- `/chat` endpoint wired to Ollama
- `/embed` endpoint
- `/ingest` endpoint for simple text/markdown ingestion
- `/rag/answer` endpoint
- LangGraph agent skeleton
- basic MLflow logging
- Qdrant collection bootstrap

## Quick start

```bash
cp .env.example .env
docker compose up -d --build
```

Pull a model on the host if needed:

```bash
ollama pull qwen3.5:9b
ollama pull nomic-embed-text
```

Health check:

```bash
curl http://localhost:8000/health
```

Chat:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Explain what this platform does."}'
```

RAG answer:

```bash
curl -X POST http://localhost:8000/rag/answer \
  -H "Content-Type: application/json" \
  -d '{"question":"What does this platform include?"}'
```

## Suggested next steps
1. Replace the simple chunker with a better document pipeline.
2. Add reranking.
3. Add tests for retrieval quality.
4. Add repo-aware code ingestion.
5. Add human approval steps to the agent graph.
