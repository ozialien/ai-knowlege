# Architecture Overview

Open WebUI -> FastAPI -> Ollama
                    -> Qdrant
                    -> MLflow
                    -> LangGraph

## Included in V4
- path and file ingestion
- source-aware citations in RAG responses
- in-memory LangGraph checkpoint plumbing
- Podman-first compose file
- Open WebUI service

## Next
- real reranker
- persistent checkpointer
- MCP tool server
