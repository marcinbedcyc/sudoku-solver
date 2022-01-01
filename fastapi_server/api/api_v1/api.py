from fastapi import APIRouter

from fastapi_server.api.api_v1.endpoints import sudoku, users, login


api_router = APIRouter()
api_router.include_router(sudoku.router, prefix='/sudoku', tags=['sudoku'])
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(login.router, prefix='/login', tags=['login'])
