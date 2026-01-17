# Librerías estándar de Python
from datetime import datetime
from typing import Optional, List,Any, Dict, Union
from enum import Enum

# Librerías de terceros
from bson import ObjectId
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, model_validator, ValidationError, field_validator


class ItemInput(BaseModel):
    model_id: str


class ItemResponse(BaseModel):
    urlModel: str
    status: str

    # El _id se convierte automáticamente a str
    class Config:
        json_encoders = {ObjectId: str}  # Convierte ObjectId a string en la respuesta




class ModelItem(BaseModel):
    id: str = Field(
        ...,
        alias="_id",
        example="01998196-edc0-78d2-996b-7f12b3cf7eb7",
        description="Identificador único del modelo"
    )

    user_assigned_name: str = Field(
        ...,
        alias="userAssignedName",
        example="Score de Riesgo",
        description="Nombre asignado por el usuario"
    )

    user_description: str = Field(
        ...,
        alias="userDescription",
        example="Puntaje crediticio basado en datos históricos",
        description="Descripción funcional del modelo"
    )

    current_status: str = Field(
        ...,
        alias="currentStatus",
        example="SERVING",
        description="Estado actual del modelo"
    )

    current_version: int = Field(
        ...,
        alias="currentVersion",
        example=1,
        description="Versión actual del modelo"
    )

    # =========================
    # Métricas (opcionales)
    # =========================

    model_total_data: Optional[int] = Field(
        None,
        alias="modelTotalData",
        example=63494,
        description="Total de registros utilizados por el modelo"
    )

    model_data_positive: Optional[int] = Field(
        None,
        alias="modelDataPositive",
        example=62171,
        description="Cantidad de registros positivos"
    )

    model_data_negative: Optional[int] = Field(
        None,
        alias="modelDataNegative",
        example=1323,
        description="Cantidad de registros negativos"
    )

    model_data_score: Optional[float] = Field(
        None,
        alias="modelDataScore",
        example=545.45,
        description="Score promedio del modelo"
    )

    ks: Optional[float] = Field(
        None,
        alias="KS",
        example=0.12,
        description="Estadístico KS del modelo"
    )

    roc_auc: Optional[float] = Field(
        None,
        alias="Roc_Auc",
        example=0.58,
        description="Área bajo la curva ROC (AUC)"
    )

    # =========================
    # Fechas y tiempos
    # =========================

    started_at: datetime = Field(
        ...,
        alias="startedAt",
        example="2025-12-22T17:09:33.382+00:00",
        description="Fecha de inicio del proceso"
    )

    ended_at: Optional[datetime] = Field(
        None,
        alias="endedAt",
        example="2025-12-22T17:09:33.382+00:00",
        description="Fecha de finalización del proceso"
    )

    time_execution_hrs: Optional[float] = Field(
        None,
        alias="timeExecutionHrs",
        example=1.59,
        description="Tiempo total de ejecución en horas"
    )

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

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
    detail: str = Field(
        "Missing finvero-user header", example="Missing finvero-user header"
    )


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


