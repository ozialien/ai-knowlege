# Architecture Overview

Open WebUI -> FastAPI -> Ollama
                    -> Qdrant
                    -> MLflow
                    -> LangGraph

## Ingestion
- raw text ingestion
- file path and directory ingestion
- code and markdown ingestion
- PDF extraction using pypdf

## Near-term extensions
- add reranker implementation
- add repo symbol extraction
- add source citations in answer formatting
- add eval datasets and regression tests
