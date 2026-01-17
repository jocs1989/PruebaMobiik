# Python estándar
import os

from typing import Optional

# Terceros
from fastapi import (
    APIRouter,
    Body,
    Request,
)


# Proyecto local
from logger import get_logger
from src.schemas.model_schema_response import (
    GetAllModels200Response,
    responses_get_all_models,
)
from src.schemas.request_schema import CreateModelRequest
from src.services.inference_service import (
    get_models_from_db,
    create_model,
)


router = APIRouter()
logger = get_logger(__name__)


@router.post("/models/create")
async def create(
    request: Request,
    data: CreateModelRequest = Body(..., description="Datos para crear el modelo"),
):
    body = data.model_dump()
    result = await create_model(request=request, body=body)
    return {"result":result}
