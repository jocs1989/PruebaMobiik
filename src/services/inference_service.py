# Librerías estándar de Python

from uuid import UUID
from fastapi import Request, HTTPException
from bson import ObjectId
from typing import Any

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

    return serialize_mongo_doc(models)


def serialize_mongo_doc(doc: Any) -> Any:
    """
    Convierte todos los ObjectId de un dict/list/objeto a str.
    Funciona recursivamente en documentos nested.
    """
    if isinstance(doc, list):
        return [serialize_mongo_doc(item) for item in doc]
    elif isinstance(doc, dict):
        return {k: serialize_mongo_doc(v) for k, v in doc.items()}
    elif isinstance(doc, ObjectId):
        return str(doc)
    else:
        return doc
