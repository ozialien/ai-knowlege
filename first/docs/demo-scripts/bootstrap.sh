#!/usr/bin/env bash
set -euo pipefail

cp -n .env.example .env || true
docker compose up -d --build

echo "Pull models on the host:"
echo "  ollama pull qwen3.5:9b"
echo "  ollama pull nomic-embed-text"
echo
echo "Ingest bundled examples:"
echo 'curl -X POST http://localhost:8000/ingest/path -H "Content-Type: application/json" -d "{"path":"/app/data/examples","source":"examples"}"'
