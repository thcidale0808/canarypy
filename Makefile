


build-api:
	docker build . -t canarypy

run-db:
	docker compose up -d

run-api: run-db
	chmod +x canarypy/api/run.py && LOG_LEVEL=debug POSTGRES_USER=postgres POSTGRES_PASSWORD=password POSTGRES_HOST=localhost POSTGRES_PORT=6543 POSTGRES_DB=canarypy canarypy/api/run.py

db-upgrade: run-db
	LOG_LEVEL=debug POSTGRES_USER=postgres POSTGRES_PASSWORD=password POSTGRES_HOST=localhost POSTGRES_PORT=6543 POSTGRES_DB=canarypy alembic upgrade head