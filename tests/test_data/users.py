from datetime import timedelta

from fastapi_server.core.security import get_password_hash, create_access_token

USERS = [
    {
        'id': 1,
        'first_name': 'Adam',
        'last_name': 'Nowak',
        'email': 'adam.nowak@poczta.pl',
        'hashed_password': get_password_hash('password'),
        'is_active': True,
        'is_superuser': False
    },
    {
        'id': 2,
        'first_name': 'Anna',
        'last_name': 'Kowalska',
        'email': 'anna.kowalska@poczta.pl',
        'hashed_password': get_password_hash('not_active123'),
        'is_active': False,
        'is_superuser': False
    },
    {
        'id': 3,
        'first_name': 'Super',
        'last_name': 'User',
        'email': 'superuser@poczta.pl',
        'hashed_password': get_password_hash('superuser_password'),
        'is_active': True,
        'is_superuser': True
    },
]

# 60 minutes * 24 hours * 365 days * 100 year = 100 year -> "never expires"
NEVER_EXPIRES_MINUTES = timedelta(minutes=60 * 24 * 365 * 100)
TOKEN_USER_0 = create_access_token(USERS[0]['id'], NEVER_EXPIRES_MINUTES)
TOKEN_USER_1 = create_access_token(USERS[1]['id'], NEVER_EXPIRES_MINUTES)
TOKEN_USER_2 = create_access_token(USERS[2]['id'], NEVER_EXPIRES_MINUTES)
WRONG_TOKEN = create_access_token(-1)  # Default expiration time
EXPIRED_TOKEN_0 = create_access_token(USERS[0]['id'], timedelta(minutes=-20))
