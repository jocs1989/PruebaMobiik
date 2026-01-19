"""Routes for API v1.""" ""


from fastapi import APIRouter

from .endpoints.model import inference
from .endpoints.auth import user
from .docs import docs_endpoinds

path = "/v1"
v1_router = APIRouter(prefix=path)

# Documentacion
v1_router.include_router(docs_endpoinds.docs_router)

#Demas endpoinds
prefix="/mobiik"
v1_router.include_router(
    inference.router, prefix=prefix, tags=["Models"]
)

v1_router.include_router(
    user.router, prefix=prefix, tags=["Users"]
)
