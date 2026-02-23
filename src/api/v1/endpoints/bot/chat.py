from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import uuid
import asyncio
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.store.postgres.aio import AsyncPostgresStore
from config import config  # Assuming your config is set up with REDIS_DB_URI

# PostgreSQL and Redis URIs
SQLALCHEMY_DATABASE_URI = "postgresql://admin:admin123@postgres:5432/core"
REDIS_URI = config.REDIS_DB_URI  # Example: redis://redis:6379/0

router = APIRouter()


class ChatRequest(BaseModel):
    user_id: str
    message: str
    thread_id: Optional[str] = None


class Context:
    def __init__(self, user_id: str):
        self.user_id = uuid.uuid4()


async def call_model(state: MessagesState):
    """Simulated call to the language model."""
    response = "Hello"  # In practice, replace with actual model call
    return {"messages": response}


# Stream messages generator function
async def stream_messages(request: ChatRequest):
    # Extract user input and optional thread ID
    user_id = uuid.uuid4().hex

    message = request.message
    thread_id = str(uuid.uuid4())  # Generate thread_id if not provided

    # Async DB interaction setup
    async with (
        AsyncPostgresStore.from_conn_string(SQLALCHEMY_DATABASE_URI) as store,
        AsyncRedisSaver.from_conn_string(REDIS_URI) as checkpointer,
    ):
        await store.setup()
        await checkpointer.setup()
        builder = StateGraph(MessagesState, context_schema=Context)
        builder.add_node(call_model)
        builder.add_edge(START, "call_model")

        graph = builder.compile(
            checkpointer=checkpointer,
            store=store,
        )

        config = {"configurable": {"thread_id": thread_id}}

        # First message stream (You can add additional steps if needed)
        async for chunk in graph.astream(
            {"messages": [{"role": "user", "content": message}]},
            config,
            stream_mode="values",
            context=Context(user_id=user_id),
        ):

            message_content = chunk["messages"][-1]
            await store.aput(
                "MEMORY",
                str(uuid.uuid4()),
                {"data": "message_content", "dato_1": 23, "api": 1},
            )  # Ensure that data is saved to PostgreSQL

            # Ensure that the message content is stringified
            message_str = (
                str(message_content)
                if not isinstance(message_content, str)
                else message_content
            )

            yield f"data: {message_str}\n\n"


# Chat stream endpoint to handle incoming requests
@router.post("/chat")
async def chat_stream(request: ChatRequest):
    """
    Endpoint to stream chat messages as Server-Sent Events.
    """
    return StreamingResponse(stream_messages(request), media_type="text/event-stream")
