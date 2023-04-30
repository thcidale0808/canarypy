export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=password
export POSTGRES_HOST=localhost
export POSTGRES_PORT=6543
export POSTGRES_DB=canarypy
alembic revision -m "add signal period column" --autogenerate
alembic upgrade head