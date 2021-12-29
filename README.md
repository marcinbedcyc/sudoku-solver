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
### Tests
1. Repeat steps 1-4 from development section
1. Run tests
    ```
    pytest
    ```
