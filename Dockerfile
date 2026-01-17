############################################
# Stage 1: Builder
############################################
FROM python:3.11-slim AS builder

ENV POETRY_VERSION=1.6.1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==$POETRY_VERSION

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

############################################
# Stage 2: Runtime
############################################
FROM python:3.11-slim AS runtime

ENV ENV=production \
    FAST_API_ENV=production \
    APP_HOME=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_DISABLE_PIP_VERSION_CHECK=on

ENV APP_ENV=${APP_ENV} \
    APP_NAME=${APP_NAME} \
    HOST=${HOST} \
    PORT=${PORT} \
    LOG_LEVEL=${LOG_LEVEL} \
    TITLE=${TITLE} \
    SWAGGER_USER=${SWAGGER_USER} \
    SWAGGER_PASS=${SWAGGER_PASS} \
    MONGODB_URI=${MONGODB_URI} \
    MONGO_MODEL_COLLECTION=${MONGO_MODEL_COLLECTION} \
    MONGO_MODEL_DB=${MONGO_MODEL_DB}

# Crear usuario no root
RUN useradd -m -d /home/usuario_template -s /bin/bash usuario_template

WORKDIR $APP_HOME

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . $APP_HOME

RUN chown -R usuario_template:usuario_template $APP_HOME

USER usuario_template

EXPOSE ${PORT}

CMD ["python", "main.py"]
