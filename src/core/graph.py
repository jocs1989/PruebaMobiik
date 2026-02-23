import logging
import uuid
from dataclasses import dataclass
from typing import Optional

from config import config
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.store.postgres.aio import AsyncPostgresStore

# -------------------------------
# Configuración de Base de Datos
# -------------------------------
SQLALCHEMY_DATABASE_URI = "host=postgres port=5432 dbname=core user=admin password=admin123"
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

    # -------------------------------
    # START
    # -------------------------------
    async def start(self):
        logger.info("Starting LangGraphAgent...")

        # --- Conexión PostgreSQL asincrónica ---
        self._store = await AsyncPostgresStore.from_conn_string(
            conn_string=self._db_uri
        ).__aenter__()
        logger.info("Connected to PostgreSQL")

        # --- Conexión Redis asincrónica ---
        self._checkpointer = await AsyncRedisSaver.from_conn_string(
            self._redis_uri
        ).__aenter__()
        logger.info("Connected to Redis")

        # --- Construcción del grafo ---
        builder = StateGraph(MessagesState, context_schema=Context)
        builder.add_node(call_model)
        builder.add_edge(START, "call_model")

        self._graph = builder.compile(
            store=self._store,
            checkpointer=self._checkpointer
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