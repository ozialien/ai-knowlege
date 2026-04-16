# AI Platform V4 Podman Starter

Podman-first local AI platform scaffold with:
- Qwen 3.5 via Ollama
- Open WebUI
- FastAPI API layer
- Qdrant vector store
- MLflow logging
- LangGraph with a checkpointer scaffold
- source-aware RAG citations

## Intent

```bash
cp .env.example .env
podman-compose up -d --build
```

Pull models on the host:

```bash
ollama pull qwen3.5:9b
ollama pull nomic-embed-text
```

Optional:
```bash
ollama pull bge-reranker-v2-m3
```

## First use

Ingest examples:

```bash
curl -X POST http://localhost:8000/ingest/path \
  -H "Content-Type: application/json" \
  -d '{"path":"/app/data/examples","source":"examples"}'
```

Ask a cited question:

```bash
curl -X POST http://localhost:8000/rag/answer \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Qdrant used for?","top_k":5}'
```

Run agent:

```bash
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{"task":"Summarize the architecture and suggest the next improvement."}'
```

Open WebUI:
- http://localhost:3000

## Notes
- The LangGraph checkpointer in this starter is in-memory. It gives you graph checkpoint plumbing but not cross-restart persistence yet.
- Reranking is still a hook, not a finished implementation.
- This repo is meant to evolve cleanly into MCP and multi-agent versions.
