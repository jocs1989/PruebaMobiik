.PHONY: run dev install shell test lint format migrate

# Variables
ENV=local
APP_ENV=local
APP_NAME=MobiikPruebaTecnica
PORT=8080
HOST= "0.0.0.0"
LOG_LEVEL=INFO
SWAGGER_USER=admin
SWAGGER_PASS=root
TITLE=Api_Template
MONGO_MODEL_DB="core"
MONGO_MODEL_COLLECTION="models"
MONGODB_URI="mongodb://mongo:27017"
MAX_LIMIT=10
SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_DB=core
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
OLLAMA_URL = "http://ollama:11434/api/generate"
MODEL_NAME = "llama2-mini"

install:
	poetry install

dev:
	poetry run uvicorn $(APP) --reload --host $(HOST) --port $(PORT) 

run:
	poetry run uvicorn $(APP) --host $(HOST) --port $(PORT) 

shell:
	poetry shell

test:
	poetry run pytest

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

migrate:
	poetry run alembic upgrade head