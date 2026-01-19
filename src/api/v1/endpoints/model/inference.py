# Python estándar
import os

from typing import Optional

# Terceros
from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    Query,
    Request,
)
import requests

# Proyecto local
from logger import get_logger
from src.schemas.model_schema_response import (
    CreateModel201Response,
    responses_create_model,
    GetAllModels200Response,
    responses_get_all_models,
)
from src.schemas.request_schema import CreateModelRequest
from src.services.inference_service import (
    get_models_from_db,
    create_model,
)
from src.schemas.llama_model_schema import AskRequest, AskResponse
from config import config

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/models/create",
    response_model=CreateModel201Response,
    responses=responses_create_model,
)
async def create(
    request: Request,
    data: CreateModelRequest = Body(..., description="Datos para crear el modelo"),
):
    body = data.model_dump()
    result = await create_model(request=request, body=body)

    logger.info(result)
    return {"result": result}


@router.get(
    "/models",
    responses=responses_get_all_models,
    response_model=GetAllModels200Response,
)
async def get_models(
    request: Request,
    limit: int = Query(10, le=100),  # Límite por defecto de 10, máximo 100
    page: int = Query(1, ge=1),  # Página por defecto 1, no puede ser menor que 1
    status: Optional[str] = Query(None, description="Filtrar por estado del modelo"),
):
    """
    Obtener modelos con soporte para paginación, filtros y limitación de resultados.
    """
    skip = (
        page - 1
    ) * limit  # Calcular cuántos documentos saltar según la página solicitada

    # Filtros opcionales

    filters = {}
    if status:
        filters["status"] = status

    try:
        # Obtener modelos de MongoDB con los filtros y paginación

        models = await get_models_from_db(
            request=request, skip=skip, limit=limit, filters=filters
        )

        result = {}
        result["result"] = models
        logger.info(result)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener los modelos: {str(e)}"
        )


@router.post("/ask", response_model=AskResponse)
def ask_model(req: AskRequest):
    payload = {
        "model": config.MODEL_NAME,
        "prompt": req.question,
        "max_tokens": 100,  # respuestas cortas para pruebas
    }
    try:
        response = requests.post(config.OLLAMA_URL, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        answer = data["results"][0]["content"]
    except Exception as e:
        answer = f"Error al consultar Ollama: {e}"
    return {"answer": answer}
