import logging
import uuid
from dataclasses import dataclass
from typing import Optional

from config import config
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.store.postgres.aio import AsyncPostgresStore
from psycopg_pool import AsyncConnectionPool
from config import config

# -------------------------------
# Configuración de Base de Datos
# -------------------------------
SQLALCHEMY_DATABASE_URI = config.SQLALCHEMY_DATABASE_URI
REDIS_URI = config.REDIS_DB_URI  # Ejemplo: redis://redis:6379/0

# -------------------------------
# Logger
# -------------------------------
logger = logging.getLogger("LangGraphAgent")
logging.basicConfig(level=logging.INFO)


# -------------------------------
# Contexto
# -------------------------------
@dataclass
class Context:
    user_id: str


# -------------------------------
# Modelo de ejemplo
# -------------------------------
async def call_model(state: MessagesState):
    """Simula llamada a modelo de lenguaje"""
    response = "Hello"
    return {"messages": response}


# -------------------------------
# LangGraphAgent
# -------------------------------
class LangGraphAgent:
    def __init__(
        self,
        db_uri: str = SQLALCHEMY_DATABASE_URI,
        redis_uri: str = REDIS_URI,
    ):
        self._db_uri = db_uri
        self._redis_uri = redis_uri
        self._store: Optional[AsyncPostgresStore] = None
        self._checkpointer: Optional[AsyncRedisSaver] = None
        self._graph: Optional[StateGraph] = None

    async def _get_connection_pool(self) -> AsyncConnectionPool:
        """Get a PostgreSQL connection pool using environment-specific settings.

        Returns:
            AsyncConnectionPool: A connection pool for PostgreSQL database.
        """
        if self._connection_pool is None:
            try:
                # Configure pool size based on environment
                max_size = config.POSTGRES_POOL_SIZE

                connection_url = (
                    "postgresql://"
                    f"{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
                    f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
                )

                self._connection_pool = AsyncConnectionPool(
                    connection_url,
                    open=False,
                    max_size=max_size,
                    kwargs={
                        "autocommit": True,
                        "connect_timeout": 5,
                        "prepare_threshold": None,
                    },
                )
                await self._connection_pool.open()
                logger.info(
                    "connection_pool_created", max_size=max_size, environment=config.ENV
                )
            except Exception as e:
                logger.error(
                    "connection_pool_creation_failed",
                    error=str(e),
                    environment=config.ENV,
                )
                # In production, we might want to degrade gracefully
                if config.ENV == "PRODUCTION":
                    logger.warning(
                        "continuing_without_connection_pool", environment=config.ENV
                    )
                    return None
                raise e
        return self._connection_pool

    # -------------------------------
    # START
    # -------------------------------
    async def start(self):
        logger.info("Starting LangGraphAgent...")

        # --- Conexión PostgreSQL asincrónica ---

        async with (
            AsyncPostgresStore.from_conn_string(self._db_uri) as store,
            AsyncPostgresSaver.from_conn_string(self._redis_uri) as checkpointer,
        ):
            logger.info("Connected to Post")
            await store.setup()
            # --- Conexión Redis asincrónica ---

            logger.info("Connected to Redis")

            await checkpointer.setup()

            # --- Construcción del grafo ---
            builder = StateGraph(MessagesState, context_schema=Context)
            builder.add_node(call_model)
            builder.add_edge(START, "call_model")

            self._graph = builder.compile(
                store=self._store, checkpointer=self._checkpointer
            )
            logger.info("LangGraphAgent ready.")

    # -------------------------------
    # SHUTDOWN
    # -------------------------------
    async def shutdown(self):
        logger.info("Shutting down LangGraphAgent...")
        try:
            if self._checkpointer:
                await self._checkpointer.__aexit__(None, None, None)
            if self._store:
                await self._store.__aexit__(None, None, None)
            logger.info("LangGraphAgent shutdown complete.")
        except Exception as e:
            logger.error(f"Error shutting down LangGraphAgent: {e}")

    # -------------------------------
    # ASK
    # -------------------------------
    async def ask(self, user_id: str, message: str, thread_id: Optional[str] = None):
        if not self._graph:
            raise RuntimeError("Agent not started. Call `await agent.start()` first.")

        thread_id = thread_id or str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}

        async for chunk in self._graph.astream(
            {"messages": [{"role": "user", "content": message}]},
            config,
            stream_mode="values",
            context=Context(user_id=user_id),
        ):
            # Retorna último mensaje
            return chunk["messages"][-1]
