# Librerías estándar de Python
import logging
import json
from uuid import UUID, uuid4
import uuid
from datetime import datetime, timezone

# Librerías de terceros
from uuid_utils import uuid7
from bson.binary import Binary, UUID_SUBTYPE
from fastapi import Request, status

# Librerías locales / del proyecto
from config import config

logger = logging.getLogger("uvicorn")


class ModelRepository:

    def __init__(self, request: Request):
        self.request = request
        self.db = request.app.mongodb_client[config.MONGO_MODEL_DB]
        self.collection = self.db[config.MONGO_MODEL_COLLECTION]

    async def create_model(self, document) -> str:

        if not isinstance(document, dict):
            raise ValueError("El documento debe ser un diccionario")

        result = await self.collection.insert_one(document=document)

        uuid_str = str(result.inserted_id)
        logging.info(f"Documento insertado con ID: {uuid_str}")

        return uuid_str

    async def get_all_models(
        self, skip: int = 0, limit: int = 10, filters: dict = None, fields: dict = None
    ):

        max_limit = int(config.MAX_LIMIT)  # Límite máximo
        limit = min(limit, max_limit)  # Asegurarse de que limit no exceda max_limit

        # Realizar la consulta
        pipeline = [
            {
                "$project": {
                    "_id": 1,
                    "model_name": 1,
                    "description": 1,
                    "model_class": 1,
                }
            },
            # {"$sort": {"campo": -1}},
            {"$skip": skip},
            {"$limit": limit},
        ]

        models_list = await self.collection.aggregate(pipeline).to_list(length=limit)

        return models_list
