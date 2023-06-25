#!/bin/bash

#This values matches the values in docker-compose.yml
export CANARYPY_DB_USER=postgres
export CANARYPY_DB_PASSWORD=password
export CANARYPY_DB_HOST=localhost
export CANARYPY_DB_PORT=6543
export CANARYPY_DB_NAME=canarypy

description=$1

if [ -z "$description" ]; then
    echo "Migration description is required."
    exit 1
fi

alembic revision --autogenerate -m "$description"