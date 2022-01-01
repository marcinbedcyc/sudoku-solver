from fastapi import APIRouter

from fastapi_server.api.api_v1.endpoits import sudoku


api_router = APIRouter()
api_router.include_router(sudoku.router, prefix='/sudoku', tags=['sudoku'])
