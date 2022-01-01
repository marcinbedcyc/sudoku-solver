from typing import Any, List

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session

from fastapi_server import crud
from fastapi_server.api.dependencies import get_db
from fastapi_server.schemas.user import User, UserCreate

router = APIRouter()


@router.get('/', response_model=List[User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    print(users)
    return users


@router.get('/{user_id}', response_model=User)
def read_user_by_id():
    pass


@router.post('/', response_model=User)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
):
    user_db = crud.user.get_by_email(db, user_in.email)
    if user_db:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='The user with this email already exists in the system.'
        )

    user_db = crud.user.create(db, user_in=user_in)
    return user_db
