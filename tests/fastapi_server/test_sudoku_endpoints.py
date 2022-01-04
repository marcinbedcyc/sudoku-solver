import pytest
from fastapi import status
from fastapi.testclient import TestClient

from fastapi_server.core.config import settings
from tests.test_data.users import (
    TOKEN_USER_0, TOKEN_USER_1, TOKEN_USER_2, EXPIRED_TOKEN_0, WRONG_TOKEN,
)


@pytest.mark.parametrize('token, sudoku_str, http_status, resturn_value', [
    # Too short sudoku string
    (
        TOKEN_USER_2,
        'too_short_string',
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {
            'detail': [
                {
                    'ctx': {'limit_value': 81},
                    'loc': ['body', 'sudoku'],
                    'msg': 'ensure this value has at least 81 characters',
                    'type': 'value_error.any_str.min_length'
                }
            ]
        }
    ),
    # Too long sudoku string
    (
        TOKEN_USER_2,
        (
            '.7846.39.6.47..1.....9.5..6.21.3748.8...9.2..3.7...6....624..7.75'
            '........3....82._too_long'
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {
            'detail': [
                {
                    'ctx': {'limit_value': 81},
                    'loc': ['body', 'sudoku'],
                    'msg': 'ensure this value has at most 81 characters',
                    'type': 'value_error.any_str.max_length'
                }
            ]
        }
    ),
    # Not allowed characters
    (
        TOKEN_USER_2,
        (
            'not_allowed47..1.....9.5..6.21.3748.8...9.2..3.7...6....624..7.75'
            '........3....82.'
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {
            'detail': [
                {
                    'ctx': {'pattern': '^[\\d\\.]+$'},
                    'loc': ['body', 'sudoku'],
                    'msg': 'string does not match regex "^[\\d\\.]+$"',
                    'type': 'value_error.str.regex'
                }
            ]
        }
    ),
    # Inactive user
    (
        TOKEN_USER_1,
        (
            '.7846.39.6.47..1.....9.5..6.21.3748.8...9.2..3.7...6....624..7.75'
            '........3....82.'
        ),
        status.HTTP_403_FORBIDDEN,
        {'detail': 'User is not active'}
    ),
    # Expired token
    (
        EXPIRED_TOKEN_0,
        (
            '.2...8..7..51..3.23..2.6.1......17.51875...9...694..8...36..8.4.4'
            '.3.2.79.59.....3'
        ),
        status.HTTP_401_UNAUTHORIZED,
        {'detail': 'Token has expired'}
    ),
    # Token for not existing user
    (
        WRONG_TOKEN,
        (
            '...34..9...5.1...49....52...6.9....2..7.6843..1.4.7.8.6...8234..2'
            '.1536..7.8...1.5'
        ),
        status.HTTP_404_NOT_FOUND,
        {'detail': 'User from token not found'}
    ),
    # Solvable
    (
        TOKEN_USER_2,
        (
            '315......4.26.5....7.4..1.9...351.2...6.9.4..1572...3......387..'
            '8.9...6...41.72..'
        ),
        status.HTTP_200_OK,
        {
            'solvable': True,
            'sudoku': (
                '31587964249261538767843215984935172623679841515724693'
                '8921563874783924561564187293'
            )
        }

    ),
    (
        TOKEN_USER_0,
        (
            '..6....1.721.59.4....3..9..9...8.46.6.8..27..1526.7.39.3..2..7..'
            '.74..68...5..8...'
        ),
        status.HTTP_200_OK,
        {
            'solvable': True,
            'sudoku': (
                '396274518721859346584361927973185462648932751152647839839526'
                '174217493685465718293'
            )
        }

    ),
    # Not solvable
    (
        TOKEN_USER_0,
        (
            '666....1.721.59.4....3..9..9...8.46.6.8..27..1526.7.39.3..2..7..'
            '.74..68...5..8...'
        ),
        status.HTTP_200_OK,
        {
            'solvable': False,
            'sudoku': (
                '666....1.721.59.4....3..9..9...8.46.6.8..27..1526.7.39.3..2..'
                '7...74..68...5..8...'
            )
        }

    )
])
def test_solve_sudoku(
    users_data,
    client: TestClient,
    token, sudoku_str, http_status, resturn_value
):
    response = client.post(
        url=f'{settings.API_V1_STR}/sudoku',
        headers={'Authorization': f'bearer {token}'},
        json={'sudoku': sudoku_str},
        allow_redirects=True
    )

    assert response.status_code == http_status
    assert response.json() == resturn_value
