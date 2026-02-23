"""FastAPI Application Initialization."""

# Librerías estándar
import logging
import os
from asyncio import gather
from contextlib import asynccontextmanager
from asyncpg import create_pool, Pool

# Librerías de terceros
from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Librerías locales / proyecto
from config import config
from logger import get_logger
from src.api.router import api_router
from src.tools.exception import CustomHTTPException
from src.database.db_connection import (
    init_mongo,
    ping_mongo_db_server,
    init_redis,
    ping_redis_server,
)

from src.models.mongo.model_document import CoreModel
from logger import get_logger
from src.database.db_connection import engine, Base
from src.database.seed import seed_roles
from src.core.graph import LangGraphAgent

# Configura el logger global
logger = get_logger(__name__)

load_dotenv(".env.dev") if os.getenv("APP_ENV") == "local" else load_dotenv(".env")

TITLE = config.APP_NAME


@asynccontextmanager
async def lifespan(app: FastAPI):

    # ---------------------------
    # MongoDB
    # ---------------------------
    app.mongodb_client = init_mongo()
    app.mongodb = app.mongodb_client[config.MONGO_MODEL_DB]

    # ---------------------------
    # Redis
    # ---------------------------
    app.redis_client = await init_redis()

    logger.info(f"Mode {config.ENV}")
    logger.info("Starting FastAPI app and connecting to databases...")

    # ---------------------------
    # PostgreSQL
    # ---------------------------
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await seed_roles(conn)
        logger.info("PostgreSQL tables created and roles seeded")

    # ---------------------------
    # Inicializar LangGraphAgent con Redis y Postgres
    # ---------------------------

    SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
    f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
)


    app.agent = LangGraphAgent(
        db_uri=SQLALCHEMY_DATABASE_URI, redis_uri=config.REDIS_DB_URI
    )
    logger.info("Starting LangGraphAgent...")
    # ---------------------------
    # Ping async databases concurrently
    # ---------------------------
    await gather(
        ping_redis_server(redis=app.redis_client),
        ping_mongo_db_server(app.mongodb),
        app.agent.start(),
    )
    logger.info(f"All databases connected successfully")

    logger.info("LangGraphAgent started successfully.")

    yield  # punto donde la app ya está lista para servir requests

    # ---------------------------
    # Shutdown: cerrar recursos
    # ---------------------------
    logger.info("Shutting down FastAPI app and closing connections...")
    await app.redis_client.close()
    app.mongodb_client.close()
    await engine.dispose()
    logger.info("All connections closed successfully")
    logger.info("Shutting down LangGraphAgent...")
    await app.agent.shutdown()
    logger.info("LangGraphAgent shutdown complete.")


def get_app():
    """Obtain FastAPI Configured Application."""
    app = FastAPI(
        title=TITLE,
        version="1.0",
        docs_url=None,
        openapi_url=None,
        redoc_url=None,
        lifespan=lifespan,
    )
    # expose_metrics(app)

    return app


app = get_app()


app.include_router(api_router)


# EndPoints for OpenAPI and Swagger UI
@app.get(path="/api/doc-json", include_in_schema=False)  # noqa: E501
def openapi_json():
    """Endpoint for OpenAPI JSON."""
    return JSONResponse(
        get_openapi(
            title=TITLE, version="1.0.0", openapi_version="3.0.0", routes=app.routes
        )
    )
