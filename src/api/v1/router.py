"""Routes for API v1.""" ""


from fastapi import APIRouter, Depends

from .endpoints.bot import chat
from .endpoints.auth import user
from .docs import docs_endpoinds
from src.authentication.security_service import get_current_user

path = "/v1"
v1_router = APIRouter(prefix=path)

# Documentacion
v1_router.include_router(docs_endpoinds.docs_router)

# Demas endpoinds
prefix = "/jocs"
v1_router.include_router(
    chat.router,
    prefix=prefix,
    tags=["Bot"],
    #dependencies=[Depends(get_current_user)], ## token
)

v1_router.include_router(user.router, prefix=prefix, tags=["Users"])
