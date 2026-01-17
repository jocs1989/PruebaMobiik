"""Routes for API v1.""" ""


from fastapi import APIRouter

from .endpoints.model import inference
from .docs import docs_endpoinds

path = "/v1"
v1_router = APIRouter(prefix=path)

# Documentacion
v1_router.include_router(docs_endpoinds.docs_router)

#Demas endpoinds

v1_router.include_router(
    inference.router, prefix="/mobiik", tags=["Models"]
)
