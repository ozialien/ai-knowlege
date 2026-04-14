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

pull-models:
	ollama pull qwen3.5:9b
	ollama pull nomic-embed-text
