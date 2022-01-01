# Sudoku solver API

### Development
1. Clone the repository
    ```
    git clone https://github.com/marcinbedcyc/sudoku-solver.git
    ```
1. Change directory to project's directory
    ```
    cd sudoku-solver
    ```
1. Ensure you have installed `poetry` (If you do not have installed poetry visit: [poetry](https://python-poetry.org/docs/#installation)) and install all dependencies and project itself.
    ```
    # Check poetry version
    poetry -V  # Expected output: Poetry version 1.1.12

    # Install app and dependencies
    poetry install
    ```
1. Activate virtual environment created by poetry
    ```
    poetry shell
    ```
1. Run migrations
    ```
    cd fastapi_server && alembic upgrade head
    ```
1. Run server
    ```
    uvicorn fastapi_server.main:app --reload
    ```
1. Add first user:
    ```
    curl -X 'POST' \
        'http://127.0.0.1:8000/api/v1/users/' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "first_name": "firstuser_name",
        "last_name": "firstuser_last_name",
        "is_active": true,
        "is_superuser": true,
        "email": "firstuser@example.com",
        "password": "password"
    }'
    ```
### Tests
1. Repeat steps 1-4 from development section
1. Ensure you are in root directory. Run tests
    ```
    pytest
    ```
