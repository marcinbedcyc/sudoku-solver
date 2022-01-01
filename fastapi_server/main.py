from fastapi import FastAPI

from fastapi_server.api.api_v1.api import api_router
from fastapi_server.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_V1_STR}/openapi.json'
)
app.include_router(api_router, prefix=settings.API_V1_STR)
