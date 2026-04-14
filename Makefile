up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

api-shell:
	docker compose exec api /bin/bash

test:
	docker compose exec api pytest -q

ingest-examples:
	curl -X POST http://localhost:8000/ingest/path \
	  -H "Content-Type: application/json" \
	  -d '{"path":"/app/data/examples","source":"examples"}'
