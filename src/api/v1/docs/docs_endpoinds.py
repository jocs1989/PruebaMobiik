import os

from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html

docs_router = APIRouter(prefix="/docs", tags=["docs"])


TITLE = os.getenv("APP_NAME", "FastAPI App")


@docs_router.get("", include_in_schema=False)
def docs():
    return get_swagger_ui_html(openapi_url="/api/doc-json", title=TITLE)
