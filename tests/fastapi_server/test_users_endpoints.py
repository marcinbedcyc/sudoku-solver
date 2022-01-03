import pytest
from fastapi import status
from fastapi.testclient import TestClient

from fastapi_server.core.config import settings
from fastapi_server.db.base import User
from tests.conftest import test_db
from tests.test_data.users import (
    EXPIRED_TOKEN_0, TOKEN_USER_0, TOKEN_USER_1, TOKEN_USER_2, WRONG_TOKEN,
    USERS
)


@pytest.mark.parametrize('token, status_code, skip, limit, data_count', [
    (TOKEN_USER_0, status.HTTP_200_OK, 0, 100, 3),
    (TOKEN_USER_0, status.HTTP_200_OK, 0, 1, 1),
    (TOKEN_USER_0, status.HTTP_200_OK, 1, 10, 2),
    (EXPIRED_TOKEN_0, status.HTTP_401_UNAUTHORIZED, 0, 100, None),
    (WRONG_TOKEN, status.HTTP_404_NOT_FOUND, 0, 100, None),
    (TOKEN_USER_1, status.HTTP_403_FORBIDDEN, 0, 100, None),
])
def test_get_users(
    users_data,
    client: TestClient,
    token, status_code, skip, limit, data_count
):
    response = client.get(
        url=f'{settings.API_V1_STR}/users',
        params={'skip': skip, 'limit': limit},
        headers={'Authorization': f'bearer {token}'}
    )

    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        response_json = response.json()
        assert len(response_json) == data_count


@pytest.mark.parametrize('token, status_code, id, user_data', [
    (TOKEN_USER_0, status.HTTP_200_OK, 1, USERS[0]),
    (TOKEN_USER_0, status.HTTP_200_OK, 2, USERS[1]),
    (TOKEN_USER_0, status.HTTP_200_OK, 3, USERS[2]),
    (TOKEN_USER_0, status.HTTP_404_NOT_FOUND, 999999, None),
    (EXPIRED_TOKEN_0, status.HTTP_401_UNAUTHORIZED, 1, None),
    (WRONG_TOKEN, status.HTTP_404_NOT_FOUND, 1, None),
    (TOKEN_USER_1, status.HTTP_403_FORBIDDEN, 1, None),
])
def test_get_user_by_id(
    users_data,
    client: TestClient,
    token, status_code, id, user_data
):
    response = client.get(
        url=f'{settings.API_V1_STR}/users/{id}',
        headers={'Authorization': f'bearer {token}'}
    )

    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        response_json = response.json()
        assert response_json['id'] == id
        assert response_json['first_name'] == user_data['first_name']
        assert response_json['last_name'] == user_data['last_name']
        assert response_json['email'] == user_data['email']
        assert response_json['is_active'] == user_data['is_active']
        assert response_json['is_superuser'] == user_data['is_superuser']
        assert not response_json.get('password')
        assert not response_json.get('hashed_password')


@pytest.mark.parametrize('user_json_data, status_code, error_detail', [
    # All's good
    (
        {
            'first_name': 'Ewelina',
            'last_name': 'Kownacka',
            'email': 'ewelina.k90@poczta.pl',
            'password': '1hgGadFY9238'
        },
        status.HTTP_201_CREATED, None
    ),
    # Incorrect email
    (
        {
            'first_name': 'Ewelina',
            'last_name': 'Kownacka',
            'email': 'wrong_email_format',
            'password': '1117ay7zcx1'
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        [{
            'loc': ['body', 'email'],
            'msg': 'value is not a valid email address',
            'type': 'value_error.email'
        }]
    ),
    # No password
    (
        {
            'first_name': 'Rozowa',
            'last_name': 'Chmurka',
            'email': 'rozowa_chmurka13@gmail.com',
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        [{
            'loc': ['body', 'password'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }]
    ),
    # Optional first name and last name
    (
        {
            'email': 'no_name_suer@poczta.pl',
            'password': '1hasdjtugGadadFY97651'
        },
        status.HTTP_201_CREATED, None
    ),
    # Email duplication
    (
        {
            'first_name': 'Ewelina',
            'last_name': 'Kownacka',
            'email': USERS[0]['email'],
            'password': '1hgGadFY9238'
        },
        status.HTTP_400_BAD_REQUEST,
        (
            f'The user with email {USERS[0]["email"]} already exists in the '
            'system.'
        )
    ),
])
def test_create_user(
    users_data,
    client: TestClient,
    user_json_data, status_code, error_detail
):
    users_count_before = len(USERS)
    response = client.post(
        url=f'{settings.API_V1_STR}/users',
        json=user_json_data,
        allow_redirects=True
    )
    assert response.status_code == status_code

    response_json = response.json()
    if status_code == status.HTTP_201_CREATED:
        if user_json_data.get('first_name'):
            assert response_json['first_name'] == user_json_data['first_name']
        if user_json_data.get('last_name'):
            assert response_json['last_name'] == user_json_data['last_name']
        assert response_json['email'] == user_json_data['email']
        assert response_json['is_active'] == user_json_data.get(
            'is_active', True
        )
        assert response_json['is_superuser'] == user_json_data.get(
            'is_superuser', False
        )
        assert not response_json.get('password')
        assert not response_json.get('hashed_password')

        response = client.get(
            url=f'{settings.API_V1_STR}/users',
            # Valid token; get users count
            headers={'Authorization': f'bearer {TOKEN_USER_0}'}
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == users_count_before + 1

    else:
        assert response_json['detail'] == error_detail


@pytest.mark.parametrize('token, id, user_data_json, http_status, detail', [
    (TOKEN_USER_2, 1, {'first_name': 'new_name'}, status.HTTP_200_OK, None),
    (
        TOKEN_USER_2,
        1,
        {'email': 'anna.kowalska@poczta.pl'},
        status.HTTP_400_BAD_REQUEST,
        (
            'The user with email anna.kowalska@poczta.pl already exists in '
            'the system.'
        )
    ),
    (
        TOKEN_USER_2,
        9990,
        {'first_name': 'new_name'},
        status.HTTP_404_NOT_FOUND,
        'User with id 9990 not found'
    ),
    (
        EXPIRED_TOKEN_0,
        1,
        {'first_name': 'new_name'},
        status.HTTP_401_UNAUTHORIZED,
        'Token has expired'
    ),
    (
        WRONG_TOKEN,
        1,
        {'first_name': 'new_name'},
        status.HTTP_404_NOT_FOUND,
        'User from token not found'
    ),
    (
        TOKEN_USER_0,
        2,
        {'first_name': 'new_name'},
        status.HTTP_403_FORBIDDEN,
        'User is not superuser'
    ),
    (
        TOKEN_USER_1,
        1,
        {'first_name': 'new_name'},
        status.HTTP_403_FORBIDDEN,
        'User is not active'
    ),
])
def test_update_user(
    users_data,
    client: TestClient,
    token, id, user_data_json, http_status, detail
):
    response = client.put(
        url=f'{settings.API_V1_STR}/users/{id}',
        headers={'Authorization': f'bearer {token}'},
        json=user_data_json,
    )

    response_json = response.json()
    if http_status == status.HTTP_200_OK:
        # TODO: More preciously data check
        assert response_json['first_name'] == user_data_json['first_name']
    else:
        assert response_json['detail'] == detail


@pytest.mark.parametrize('token, id, http_status, detail', [
    (TOKEN_USER_2, 1, status.HTTP_200_OK, None),
    (
        TOKEN_USER_2,
        123123,
        status.HTTP_404_NOT_FOUND,
        'User with id 123123 not found'
    ),
    (EXPIRED_TOKEN_0, 1, status.HTTP_401_UNAUTHORIZED, 'Token has expired'),
    (WRONG_TOKEN, 1, status.HTTP_404_NOT_FOUND, 'User from token not found'),
    (TOKEN_USER_0, 2, status.HTTP_403_FORBIDDEN, 'User is not superuser'),
    (TOKEN_USER_1, 1, status.HTTP_403_FORBIDDEN, 'User is not active'),
])
def test_remove_user(
    users_data,
    client: TestClient,
    token, id, http_status, detail
):
    users_count_before = len(USERS)
    response = client.delete(
        url=f'{settings.API_V1_STR}/users/{id}',
        headers={'Authorization': f'bearer {token}'}
    )

    assert response.status_code == http_status

    if http_status == status.HTTP_200_OK:
        with test_db() as db:
            assert users_count_before == len(db.query(User).all()) + 1

    else:
        assert response.json()['detail'] == detail
