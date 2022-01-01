from datetime import datetime, timedelta, timezone
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from fastapi_server.core.config import settings

password_crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any],
    expires_delta: timedelta = None
) -> str:
    if expires_delta:
        # Using now(timezone.utc) instead utcnow(), because:
        # https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_crypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_crypt_context.hash(password)
