import logging
import os
from motor.motor_asyncio import AsyncIOMotorClient
from logger import get_logger
from config import config
from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import AsyncGenerator
from sqlalchemy.orm import relationship, declarative_base

# MONGO
logger = logging.getLogger("uvicorn")


logger = get_logger(__name__)


def init_mongo():
    env = os.getenv("ENV", "local").lower()

    if env == "production":
        logger.info("Mongo mod PROD")
        return AsyncIOMotorClient(
            config.MONGODB_URI, tls=True, tlsAllowInvalidCertificates=True
        )

    elif env == "local":
        logger.info("Mongo mod LOCAL")
        return AsyncIOMotorClient(config.MONGODB_URI)

    else:
        raise ValueError(
            f"ENV '{env}' is not supported. Set ENV to 'development', 'staging' or 'production'."
        )


async def ping_mongo_db_server(database):
    ping_response = await database.command("ping")
    if int(ping_response["ok"]) != 1:

        raise Exception("Problem connecting to database cluster.")

    else:

        logger.info("Connected to database cluster.")


#########################################################################
# async def ping_elasticsearch_server():
#     try:
#         await es_client.info()
#         logger.info(
#             "Elasticsearch connection successful"
#         )
#     except TransportError as e:
#         logger.error(
#             f"Elasticsearch connection failed: {e}"
#         )
#         raise e


# Redis
async def init_redis() -> Redis:
    env = os.getenv("ENV", "development").lower()

    if env == "production":
        logger.info("Redis mod PROD")
        redis_url = config.REDIS_URL  # Asegúrate de tener esto en tu config
        return Redis.from_url(
            redis_url, max_connections=100
        )  # <- asegúrate de que esté en False o eliminado)

    elif env == "local":
        logger.info("Redis mod LOCAL")
        redis_url = "redis://redis:6379"  # Asegúrate de tener esto en tu config
        return Redis.from_url(
            redis_url, max_connections=100
        )  # <- asegúrate de que esté en False o eliminado)

    else:
        raise ValueError(
            f"ENV '{env}' is not supported. Set ENV to 'production' or 'local'."
        )


async def ping_redis_server(redis: Redis):
    try:
        await redis.ping()
        logger.info("Connected to Redis")
    except Exception as e:
        logger.error(f"Error connecting to Redis: {e}")
        raise e


# Postgrest


SQLALCHEMY_DATABASE_URI = (
    f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
    f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
)

engine: AsyncEngine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=True,
    pool_size=20,
    max_overflow=10,
)

Base = declarative_base()

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session