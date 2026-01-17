"""FastAPI Application Initialization."""

# Librerías estándar
import logging
import os
from asyncio import gather
from contextlib import asynccontextmanager

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

from src.models.model_document import CoreModel
from logger import get_logger


# Configura el logger global
logger = get_logger(__name__)

load_dotenv(".env.dev") if os.getenv("APP_ENV") == "local" else load_dotenv(".env")

TITLE = config.APP_NAME


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = init_mongo()
    app.mongodb = app.mongodb_client[config.MONGO_MODEL_DB]
    app.redis_client = await init_redis()
    logger_uvicorn = logging.getLogger("uvicorn")
    logger_uvicorn.info(f"Mode {config.ENV}")
    # eventhub

    await gather(
        ping_redis_server(redis=app.redis_client),
        ping_mongo_db_server(app.mongodb),
    )
    logger_uvicorn.info(f"Connected to database {config.MONGO_MODEL_DB}")

    yield
    app.mongodb_client.close()

    # await eventhub_service.stop()


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
