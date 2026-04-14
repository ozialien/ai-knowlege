# AI Platform V3 Starter

A stronger local AI engineering scaffold with:
- Ollama + Qwen 3.5 for local chat
- Qdrant vector store
- FastAPI API layer
- MLflow logging
- LangGraph agent skeleton
- file and repo ingestion
- optional reranking hook
- Docker Compose for local orchestration

## Features
- `/chat` local chat endpoint
- `/embed` embeddings endpoint
- `/ingest/texts` raw text ingestion
- `/ingest/path` directory and repo ingestion
- `/rag/answer` retrieval-augmented answering
- `/agent/run` LangGraph agent skeleton
- smoke tests and example documents

## Quick start

```bash
cp .env.example .env
docker compose up -d --build
```

Pull models on the host:

```bash
ollama pull qwen3.5:9b
ollama pull nomic-embed-text
```

Optional reranker model for later:
```bash
ollama pull bge-reranker-v2-m3
```

## Suggested usage

1. Ingest bundled docs:
```bash
curl -X POST http://localhost:8000/ingest/path \
  -H "Content-Type: application/json" \
  -d '{"path":"/app/data/examples","source":"examples"}'
```

2. Ask a grounded question:
```bash
curl -X POST http://localhost:8000/rag/answer \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Qdrant used for?","top_k":5}'
```

3. Run the simple agent:
```bash
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{"task":"Summarize the platform architecture and suggest the next improvement."}'
```

## Notes
- PDF support is included via `pypdf`.
- The reranker is optional and currently implemented as a hook. The default path works without it.
- Code/repo ingestion is conservative by default and skips noisy/generated files.
