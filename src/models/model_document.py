from beanie import Document, View
from pydantic import BaseModel, Field, constr, conint

from typing import Optional, List, Dict, Any, Union, Literal
from datetime import datetime
from bson import ObjectId
import uuid


# ➤ Modelo principal
class CoreModel(Document):
    id: bytes = Field(
        default_factory=ObjectId,
        alias="_id",
        title="Model Identifier",
        description=(
            "Descripción: Identificador único del documento. En este caso hace referencia al identificador "
            "único del modelo creado.\n\n"
            "Consideraciones: Debe de ser UUID v7 válido en formato binario.\n\n"
            "Ejemplo: 0197d68a-64dd-78a2-bc95-17e0b150771f"
        ),
    )

    name: constr(
        min_length=32,
        max_length=32,
        pattern=r"^[0-9a-f]{8}[0-9a-f]{4}4[0-9a-f]{3}[89ab][0-9a-f]{3}[0-9a-f]{12}$",
    ) = Field(
        ...,
        title="Model Name",
        description="UUID v4 en formato hex (32 caracteres, sin guiones). Ej: 0197d68a64dd78a2bc9517e0b150771f",
    )

    userAssignedName: constr(min_length=5, max_length=100) = Field(
        ...,
        title="User Assigned Name",
        description=(
            "Descripción: Nombre de modelo asignado por el usuario.\n\n"
            "Ejemplo: Modelo Originacion V1"
        ),
    )

    userDescription: Optional[constr(max_length=200)] = Field(
        None,
        title="User description",
        description=(
            "Descripción: Descripción del modelo asignada por el usuario.\n\n"
            "Ejemplo: Modelo de ML para la originacion de credito"
        ),
    )

    class Settings:
        name = "core"

    model_config = {
        "extra": "forbid",
        "arbitrary_types_allowed": True,
        "json_encoders": {bytes: lambda v: str(uuid.UUID(bytes=v))},
    }
