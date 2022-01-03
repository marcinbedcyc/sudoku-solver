import pytest  # noqa
from fastapi import status
from fastapi.testclient import TestClient

from fastapi_server.core.config import settings
from tests.test_data.users import (
    TOKEN_USER_0, TOKEN_USER_1, TOKEN_USER_2, USERS, WRONG_TOKEN,
    EXPIRED_TOKEN_0
)


@pytest.mark.parametrize('username, password, status_code, error_detail', [
    ('adam.nowak@poczta.pl', 'password', status.HTTP_200_OK, None),
    (
        'adam.nowak@poczta.pl',
        'bad_password',
        status.HTTP_400_BAD_REQUEST,
        'Incorrect username or password'
    ),
    (
        'anna.kowalska@poczta.pl',
        'not_active123',
        status.HTTP_400_BAD_REQUEST,
        'Inactive user'
    ),
    ('superuser@poczta.pl', 'superuser_password', status.HTTP_200_OK, None),
])
def test_login_endpoints(
    users_data,
    client: TestClient,
    username,
    password,
    status_code,
    error_detail
):
    response = client.post(
        url=f'{settings.API_V1_STR}/login/access-token',
        data={'username': username, 'password': password}
    )
    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        response_json = response.json()
        assert 'access_token' in response_json
        assert 'token_type' in response_json
        assert response_json['token_type'] == 'bearer'
    else:
        response_json = response.json()
        assert response_json['detail'] == error_detail


@pytest.mark.parametrize('token, status_code, user_dict', [
    (TOKEN_USER_0, status.HTTP_200_OK, USERS[0]),
    (TOKEN_USER_1, status.HTTP_200_OK, USERS[1]),
    (TOKEN_USER_2, status.HTTP_200_OK, USERS[2]),
    (WRONG_TOKEN, status.HTTP_404_NOT_FOUND, USERS[0]),
    (EXPIRED_TOKEN_0, status.HTTP_401_UNAUTHORIZED, USERS[0]),
])
def test_login_token_test(
    users_data,
    client: TestClient,
    token,
    status_code,
    user_dict: dict
):
    response = client.post(
        url=f'{settings.API_V1_STR}/login/test-token',
        headers={'Authorization': f'bearer {token}'}
    )
    print(response.json())
    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        assert response.json()
        response_json = response.json()
        if user_dict.get('first_name'):
            assert response_json['first_name'] == user_dict['first_name']
        if user_dict.get('last_name'):
            assert response_json['last_name'] == user_dict['last_name']
        assert response_json['email'] == user_dict['email']
        assert response_json['is_active'] is user_dict['is_active']
        assert response_json['is_superuser'] is user_dict['is_superuser']
        assert response_json['id'] == user_dict['id']
