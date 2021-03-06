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

additional_responses = {
    '401': {
        'description': 'Unauthorized',
        'content': {
            'application/json': {
                'examples': {
                    'not_authenticated': {
                        'summary': ' Not authenticated user',
                        'value': {'detail': 'Not authenticated'}
                    },
                    'token_expired': {
                        'summary': 'Expired token',
                        'value': {'detail': 'Token has expired'}
                    }
                }
            }
        }
    },
    '403': {
        'description': 'Forbidden access',
        'content': {
            'application/json': {
                'examples': {
                    'not_valid_credentials': {
                        'summary': 'Not valid credentials',
                        'value': {'detail': 'Could not validate credentials'}
                    }
                }
            }
        }
    },
    '404': {
        'description': 'User from token not found',
        'content': {
            'application/json': {
                'examples': {
                    'not_found': {
                        'summary': 'Current user not found',
                        'value': {'detail': 'User from token not found'}
                    }
                }
            }
        }
    }
}

not_active_response = {
    'not_active': {
        'summary': 'Not active user',
        'value': {'detail': 'User is not active'}
    }
}

not_active_superuser_response = {
    'not_active_superuser': {
        'summary': 'Not active superuser',
        'value': {'detail': 'User is not active superuser'}
    }
}


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
    # Token has expired
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token has expired'
        )
    # Invalid credentials - cannot decode or load into object.
    except (jwt.JWTError, ValidationError, jwt.JWTClaimsError):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail='Could not validate credentials'
        )

    # Get user
    user = crud.user.get(db, id=token_data.sub)

    # Raise an error if user does not exist.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User from token not found'
        )

    return user


def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    if not crud.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User is not active'
        )

    return user


def get_current_active_superuser(
    user: User = Depends(get_current_active_user)
) -> User:
    if not crud.user.is_superuser(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User is not superuser'
        )

    return user
