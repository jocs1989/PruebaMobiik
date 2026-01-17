# Librerías estándar de Python

from uuid import UUID
from fastapi import Request, HTTPException


# Librerías de terceros
from fastapi import Request


# Librerías locales / del proyecto

from logger import get_logger
from src.repositories.model_repository import ModelRepository
from src.schemas.model_schema_response import CustomHTTPException


logger = get_logger(__name__)


# Función para obtener modelos con paginación, filtros y proyección




async def create_model(request: Request, body: dict):
    logger.info("🟡 Inicio de inicialización del esquema del modelo")

    try:
        repository = ModelRepository(request=request)
        model_id = await repository.create_model(document=body)
    except Exception:
        logger.exception("❌ Error al guardar modelo")
        raise CustomHTTPException(500, "Error al guardar modelo")

    return {
        "_id": model_id,
        "status": "INITIALIZING",
    }


async def get_models_from_db(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    filters: dict = None,
    fields: dict = None,
):
    model_repository = ModelRepository(request=request)
    models = await model_repository.get_all_models(
        skip=skip, limit=limit, filters=filters, fields=fields
    )
    total_items = await model_repository.get_total_models()
    current_page = (skip // limit) + 1
    total_pages = (total_items + limit - 1) // limit
    data = process_models(models)

    return {
        "data": data,
        "totalItems": total_items,
        "currentPage": current_page,
        "totalPages": total_pages,
    }

