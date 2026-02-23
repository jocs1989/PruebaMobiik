from fastapi import APIRouter, Body, Request, HTTPException
from typing import Any
from pydantic import BaseModel
from typing import Optional, Any
router = APIRouter()


class ChatRequest(BaseModel):
    user_id: str
    message: str
    thread_id: Optional[str] = None


@router.post(
    "/chat"
)  # response_model=None por defecto si no quieres validación de salida
async def chat(request: Request, data: ChatRequest = Body(...)):
    agent = request.app.agent

    if not agent._graph:
        raise HTTPException(status_code=503, detail="Agent not ready")

    # Llamada al agente
    response = await agent.ask(
        user_id=data.user_id, message=data.message, thread_id=data.thread_id
    )

    # Convierte a dict si es un objeto Pydantic, o a string si no
    return {"response": response.dict() if hasattr(response, "dict") else str(response)}
