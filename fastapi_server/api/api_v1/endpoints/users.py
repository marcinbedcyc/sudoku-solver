from copy import deepcopy
from typing import Any, List, Optional

from fastapi import APIRouter, HTTPException, status, Query, Path
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session

from fastapi_server import crud
from fastapi_server.api.dependencies import (
    get_db,
    get_current_active_user,
    get_current_active_superuser,
    additional_responses,
    not_active_response,
    not_active_superuser_response
)
from fastapi_server.models import User as UserModel
from fastapi_server.schemas import User, UserCreate, UserUpdate

router = APIRouter()

bad_request_not_unique_email = {
    'description': 'Bad request',
    'content': {
        'application/json': {
            'examples': {
                'not unique email': {
                    'summary': 'Not unique email value',
                    'value': {
                        'detail': (
                            'The user with email testuser@example.com already '
                            'exists in the system.'
                        )
                    }
                }
            }
        }
    }
}

# Update read users response examples with not active user response
read_users_responses = deepcopy(additional_responses)
read_users_responses['403']['content']['application/json']['examples'].update(
    not_active_response
)


@router.get(
    '/',
    response_model=List[User],
    summary='Get users from database',
    responses=read_users_responses
)
def read_users(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
    skip: Optional[int] = Query(0, ge=0, description='Skip N first records'),
    limit: Optional[int] = Query(
        100, gt=0, description='Max number of records'
    )
) -> Any:
    """
    Get list of users from database. Only allowed for active and authenticated
    users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


read_user_responses = deepcopy(read_users_responses)
read_user_responses['404']['content']['application/json']['examples'].update({
    'not found': {
        'summary': 'User not found',
        'value': {'detail': 'User with id 1 not found'}
    }
})


@router.get(
    '/{user_id}',
    response_model=User,
    responses=read_user_responses,
    summary='Read user\'s data with given id'
)
def read_user_by_id(
    user_id: int = Path(..., gt=0, description='User\'s primary key - id'),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """Get user's data with the given id if exists."""
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {user_id} not found'
        )
    return user


@router.post(
    '/',
    response_model=User,
    responses={status.HTTP_400_BAD_REQUEST: bad_request_not_unique_email}
)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate
) -> Any:
    """
    Create user with the given data. E-mail has to be unique value per user.
    """
    user_db = crud.user.get_by_email(db, user_in.email)
    if user_db:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=(
                f'The user with email {user_in.email} already exists in the '
                'system.'
            )
        )

    user_db = crud.user.create(db, user_in=user_in)
    return user_db


update_user_responses = deepcopy(additional_responses)
update_user_responses['403']['content']['application/json']['examples'].update(
    {**not_active_superuser_response, **not_active_response}
)
update_user_responses['404']['content']['application/json']['examples'].update(
    {
        'not found': {
            'summary': 'User not found',
            'value': {'detail': 'User with id 1 not found'}
        }
    }
)
update_user_responses['400'] = bad_request_not_unique_email


@router.put('/{user_id}', response_model=User, responses=update_user_responses)
def update_user(
    *,
    user_in: UserUpdate,
    user_id: int = Path(..., gt=0, description='User\'s primary key - id'),
    db: Session = Depends(get_db),
    current_superuser: User = Depends(get_current_active_superuser)
) -> Any:
    """Update user's record with given data. Endpoint only for superusers"""
    user_db = crud.user.get(db, id=user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {user_id} not found'
        )
    if (
        user_in.email != user_db.email and
        crud.user.get_by_email(db, user_in.email)
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=(
                f'The user with email {user_in.email} already exists in the '
                'system.'
            )
        )
    user_db = crud.user.update(db, user_db=user_db, user_in=user_in)
    return user_db


delete_user_responses = deepcopy(additional_responses)
delete_user_responses['403']['content']['application/json']['examples'].update(
    {**not_active_superuser_response, **not_active_response}
)
delete_user_responses['404']['content']['application/json']['examples'].update(
    {
        'not found': {
            'summary': 'User not found',
            'value': {'detail': 'User with id 1 not found'}
        }
    }
)


@router.delete(
    '/{user_id}',
    response_model=User,
    responses=delete_user_responses
)
def remove_user(
    *,
    user_id: int = Path(..., gt=0, description='User\'s primary key - id'),
    db: Session = Depends(get_db),
    current_superuser: User = Depends(get_current_active_superuser)
):
    """
    Delete user's data with the given id if exists. Only superuser can delete
    data.
    """
    user_db = crud.user.get(db, id=user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {user_id} not found'
        )

    user_db = crud.user.remove(db, user_db)
    return user_db
