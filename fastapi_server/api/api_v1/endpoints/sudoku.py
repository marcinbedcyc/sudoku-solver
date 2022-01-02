from fastapi import APIRouter
from fastapi.params import Body, Depends

from fastapi_server.models import User
from fastapi_server.schemas import SudokuIn, SudokuOut
from fastapi_server.api.dependencies import get_current_user
from sudoku_solver.solver import (
    is_valid_sudoku_grid,
    solve_sudoku,
    sudoku_str_to_grid,
    grid_to_sudoku_str,
)


router = APIRouter()


@router.post(
    '/',
    response_model=SudokuOut,
    summary='Solve the sudoku',
    description='Solve the sudoku if it is possible and return the solution.',
)
def solve(
    current_user: User = Depends(get_current_user),
    sudoku_in: SudokuIn = Body(
        ...,
        examples={
            'dots': {
                'summary': (
                    'Correct data using dots with solution (the most readable '
                    'for humans).'
                ),
                'value': {
                    'sudoku': (
                        '..98..7.41..5..6...3...7.9.5.27.8.3..81.5...664.123.'
                        '5....24.3..9..6.18....5..9.2.'
                    ),
                }
            },
            'zeros': {
                'summary': 'Correct data using zeros with solution.',
                'value': {
                    'sudoku': (
                        '0098007041005006000300070905027080300810500066401230'
                        '50000240300900601800005009020'
                    ),
                }
            },
            'too_short': {
                'summary': 'Too short sudoku\'s string',
                'value': {
                    'sudoku': '..98..7.41..5..6...3..7.9..5..123.',
                }
            },
            'too_long': {
                'summary': 'Too long sudoku\'s string',
                'value': {
                    'sudoku': (
                        '..12..3.4552..5..6...3...7.98.3..81.5...1652.12321.'
                        '5..5..9.2....478...2.18.39....687..1..4..2'
                    ),
                }
            },
            'not_allowed_characters': {
                'summary': 'With not allowed characters',
                'value': {
                    'sudoku': (
                        '..ab.cd.ed.fg.hi..jk...7.9.5.27.8.3..81.5...664.123.'
                        '5....24.3..9..6.18....5..9.2.'
                    ),
                }
            },
        }
    )
):
    grid = sudoku_str_to_grid(sudoku_in.dict()['sudoku'])
    solvable = is_valid_sudoku_grid(grid)
    if solvable:
        solve_sudoku(grid)
    return SudokuOut(sudoku=grid_to_sudoku_str(grid), solvable=solvable)
