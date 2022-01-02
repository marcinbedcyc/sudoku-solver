from typing import Generator

from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session

from fastapi_server import crud
from fastapi_server.core.config import settings
from fastapi_server.core.security import ALGORITHM
from fastapi_server.db.session import SessionLocal
from fastapi_server.models import User
from fastapi_server.schemas import TokenPayload


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_V1_STR}/login/access-token'
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema)
) -> User:
    # Decode token and create schema TokenPayload object
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    # Invalid credentials - cannot decode or load into object.
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail='Could not validate credentials'
        )

    # Get user
    user = crud.user.get(db, id=token_data.sub)

    # Raise an error if user does not exist.
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User not found')

    return user
