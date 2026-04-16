up:
	podman-compose up -d --build

down:
	podman-compose down

logs:
	podman-compose logs -f

ps:
	podman-compose ps

api-shell:
	podman-compose exec api /bin/bash

test:
	podman-compose exec api pytest -q

ingest-examples:
	curl -X POST http://localhost:8000/ingest/path \
	  -H "Content-Type: application/json" \
	  -d '{"path":"/app/data/examples","source":"examples"}'
