# AI Learning Lab (Podman-first)

A single repo for learning modern local AI systems from the ground up with runnable, inspectable examples.

## What this teaches

This lab is organized as a ladder:

1. **Inference** — call a local model through Ollama
2. **Embeddings** — convert text into vectors
3. **Vector DB** — store and search embeddings in Qdrant
4. **RAG** — retrieve context, then generate grounded answers
5. **Agent Graphs** — plan/respond workflow with LangGraph
6. **Memory & Checkpoints** — thread state and checkpoint plumbing
7. **Human-in-the-loop** — approval boundary patterns
8. **MCP shape** — protocol-friendly tool boundary
9. **Multi-agent split** — retrieval, code, ops boundaries
10. **Observability** — basic MLflow logging

## Quick start

```bash
cp .env.example .env
podman-compose up -d --build
ollama pull qwen3.5:9b
ollama pull nomic-embed-text
```

Open:
- API docs: http://localhost:8000/docs
- Open WebUI: http://localhost:3000
- MLflow: http://localhost:5000

## Honest caveats

- The MCP portion is a teaching stub, not a full MCP SDK integration.
- The multi-agent section is an architectural split, not a standards-compliant A2A transport.
- The LangGraph checkpointing in this starter uses in-memory storage, so it does not persist across container restarts.
