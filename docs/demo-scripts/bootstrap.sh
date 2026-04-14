#!/usr/bin/env bash
set -euo pipefail

cp -n .env.example .env || true
docker compose up -d --build

echo "When Ollama is ready, pull models:"
echo "  ollama pull qwen3.5:9b"
echo "  ollama pull nomic-embed-text"
echo
echo "Then ingest sample docs:"
echo 'curl -X POST http://localhost:8000/ingest -H "Content-Type: application/json" -d "{"texts":["Local AI platforms use retrieval and evaluation."],"source":"demo"}"'
