# Librerías estándar de Python
import logging

# Librerías de terceros
from fastapi import Request, status,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware



# Configurar el logger
logger = logging.getLogger(__name__)



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
