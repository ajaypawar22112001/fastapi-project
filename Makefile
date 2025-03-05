.PHONY: applyMigration createMigration runLocal runBuildDocker runDocker runTest

SHELL := /bin/bash

applyMigration:
	source .env.local && \
	poetry run alembic upgrade head

createMigration:
	source .env.local && \
	poetry run alembic revision --autogenerate -m "new migration"

runLocal:
	source .env && \
	poetry run uvicorn fastapi_server.server:app --port 1140 --reload --host 0.0.0.0

runBuildDocker:
	docker compose --env-file ./.env.local -f docker-compose.yml up -d --build

runDocker:
	docker compose --env-file ./.env.local -f docker-compose.yml up -d

runTest:
	source .env.local && \
	pytest --cov=master_server --cov-fail-under=90 -vv tests/