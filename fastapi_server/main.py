from fastapi import FastAPI

from fastapi_server.api.api_v1.api import api_router


app = FastAPI()
app.include_router(api_router)
