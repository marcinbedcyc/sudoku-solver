from typing import Any
from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi_server import crud
from fastapi_server.core import security
from fastapi_server.api.dependencies import (
    additional_responses,
    get_db, get_current_user
)
from fastapi_server.core.config import settings
from fastapi_server.models import User as UserModel
from fastapi_server.schemas import Token, User

router = APIRouter()


@router.post('/access-token', response_model=Token, responses={
    status.HTTP_400_BAD_REQUEST: {
        'description': 'Bad request',
        'content': {
            'application/json': {
                'examples': {
                    'incorrect_credentials': {
                        'summary': 'Incorrect credentials',
                        'value': {'detail': 'Incorrect username or password'}
                    },
                    'inactive_user': {
                        'summary': 'Inactive user',
                        'value': {'detail': 'Inactive user'}
                    },
                }
            }
        }
    }
})
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """OAuth2 compatible token login get an access token for future requests"""
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='Incorrect username or password'
        )
    elif not crud.user.is_active(user):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail='Inactive user'
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {
        'access_token': security.create_access_token(
            user.id,
            expires_delta=access_token_expires
        ),
        'token_type': 'bearer'
    }


@router.post(
    '/test-token',
    response_model=User,
    responses=additional_responses
)
def test_token(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Test access token"""
    return current_user
