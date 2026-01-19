# Librerías estándar de Python
from datetime import datetime
from typing import Optional, List, Any, Dict, Union
from enum import Enum

# Librerías de terceros
from bson import ObjectId
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)

## Create


# =========================
# Model Item
# =========================


class ModelItem(BaseModel):
    id: str = Field(
        ...,
        alias="_id",
        example="507f1f77bcf86cd799439011",
        description="Identificador único del modelo",
    )
    status: str

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


# =========================
# Create Model Responses
# =========================


class CreateModel201Response(BaseModel):
    status: str = Field(
        "success", example="success", description="Estado de la solicitud"
    )
    detail: str = Field(
        "Modelo creado correctamente",
        example="Modelo creado correctamente",
        description="Mensaje informativo del resultado",
    )
    result: ModelItem = Field(..., description="Modelo creado")


class CreateModel400Response(BaseModel):
    status: str = Field("failed", example="failed")
    detail: str = Field("Solicitud incorrecta", example="Solicitud incorrecta")


class CreateModel401Response(BaseModel):
    status: str = Field("failed", example="failed")
    detail: str = Field("Missing  header", example="Missing header")


class CreateModel403Response(BaseModel):
    status: str = Field("failed", example="failed")
    detail: str = Field("Permission denied", example="Permission denied")


class CreateModel500Response(BaseModel):
    status: str = Field("failed", example="failed")
    detail: str = Field(
        "No se pudo crear el modelo",
        example="No se pudo crear el modelo. Contacte con soporte.",
    )


class CreateModel503Response(BaseModel):
    status: str = Field("503 Service Unavailable", example="503 Service Unavailable")
    detail: str = Field(
        "Servicio no disponible temporalmente",
        example="Servicio no disponible temporalmente. Intente más tarde.",
    )


responses_create_model = {
    status.HTTP_201_CREATED: {
        "model": CreateModel201Response,
        "description": "Modelo creado correctamente",
    },
    status.HTTP_400_BAD_REQUEST: {"model": CreateModel400Response},
    status.HTTP_401_UNAUTHORIZED: {"model": CreateModel401Response},
    status.HTTP_403_FORBIDDEN: {"model": CreateModel403Response},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": CreateModel500Response},
    status.HTTP_503_SERVICE_UNAVAILABLE: {"model": CreateModel503Response},
}

###############################3
##############################3


class ItemInput(BaseModel):
    model_id: str


class ItemResponse(BaseModel):
    urlModel: str
    status: str

    # El _id se convierte automáticamente a str
    class Config:
        json_encoders = {ObjectId: str}  # Convierte ObjectId a string en la respuesta

class ModelItem(BaseModel):
    id: str= Field(
        ...,
        alias="_id",
        example="01998196-edc0-78d2-996b-7f12b3cf7eb7",
        description="Identificador único del modelo",
    )
    model_name: str
    description: str
    model_class: List[str]

    model_config = ConfigDict(
        populate_by_name=True,  # equivale a allow_population_by_field_name
        json_encoders={ObjectId: str},  # json_encoders sigue funcionando
        serialize_by_alias=True
    )
 
# =========================
# Success Response
# =========================


class GetAllModels200Response(BaseModel):
    status: str = Field(
        "success", example="success", description="Estado de la solicitud"
    )
    detail: str = Field(
        "Modelos obtenidos correctamente",
        example="Modelos obtenidos correctamente",
        description="Mensaje informativo del resultado",
    )
    result: List[ModelItem] = Field(
        ..., description="Lista de todos los modelos disponibles"
    )


class GetAllModels400Response(BaseModel):
    status: str = Field("failed", example="failed")
    detail: str = Field("Solicitud incorrecta", example="Solicitud incorrecta")


class GetAllModels401Response(BaseModel):
    status: str = Field("failed", example="failed")
    detail: str = Field("Missing header", example="Missing  header")


class GetAllModels403Response(BaseModel):
    status: str = Field("failed", example="failed")
    detail: str = Field("Permission denied", example="Permission denied")


class GetAllModels404Response(BaseModel):
    status: str = Field("failed", example="failed")
    detail: str = Field(
        "No se encontraron modelos", example="No se encontraron modelos"
    )


class GetAllModels500Response(BaseModel):
    status: str = Field("failed", example="failed")
    detail: str = Field(
        "No se pudieron obtener los modelos",
        example="No se pudieron obtener los modelos. Contacte con soporte.",
    )


class GetAllModels503Response(BaseModel):
    status: str = Field("503 Service Unavailable", example="503 Service Unavailable")
    detail: str = Field(
        "Servicio no disponible temporalmente",
        example="Servicio no disponible temporalmente. Intente más tarde.",
    )


responses_get_all_models = {
    status.HTTP_200_OK: {
        "model": GetAllModels200Response,
        "description": "Lista de todos los modelos",
    },
    status.HTTP_400_BAD_REQUEST: {"model": GetAllModels400Response},
    status.HTTP_401_UNAUTHORIZED: {"model": GetAllModels401Response},
    status.HTTP_403_FORBIDDEN: {"model": GetAllModels403Response},
    status.HTTP_404_NOT_FOUND: {"model": GetAllModels404Response},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": GetAllModels500Response},
    status.HTTP_503_SERVICE_UNAVAILABLE: {"model": GetAllModels503Response},
}


class ErrorResponse(BaseModel):
    detail: str = Field(
        "Se produjo un error",
        example="No se encontraron modelos",
        description="Mensaje de error que describe lo que ocurrió.",
    )
    status: str = Field(
        "failed", example="Failed", description="Estado de la solicitud."
    )


class CustomHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str = "Se produjo un error",
        status: str = "failed",
    ):
        # Crear la respuesta usando el modelo ErrorResponse
        self.response_body = ErrorResponse(detail=detail, status=status)

        # Pasar el `detail` a la clase base (FastAPI lo usa para crear la respuesta de error)
        super().__init__(status_code=status_code, detail=detail)

    def get_response(self):
        # Devolver la respuesta JSON con el cuerpo personalizado
        return JSONResponse(
            content=self.response_body.dict(), status_code=self.status_code
        )
