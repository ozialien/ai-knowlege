up:
	podman-compose up -d --build

down:
	podman-compose down

logs:
	podman-compose logs -f

ps:
	podman-compose ps

ingest:
	curl -X POST http://localhost:8000/lesson/03/ingest_examples

rag:
	curl -X POST http://localhost:8000/lesson/03/rag_answer \
	  -H "Content-Type: application/json" \
	  -d '{"question":"What is Qdrant used for?"}'

agent:
	curl -X POST http://localhost:8000/lesson/04/agent_run \
	  -H "Content-Type: application/json" \
	  -d '{"task":"Summarize the architecture and suggest the next improvement."}'
