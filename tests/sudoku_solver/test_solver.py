import pytest
from contextlib import contextmanager

from sudoku_solver.solver import (
    is_valid_column,
    is_valid_row,
    is_valid_boxes,
    is_valid_sudoku_grid,
    grid_to_sudoku_str,
    sudoku_str_to_grid,
    is_safe,
    solve_sudoku,
    InvalidSudokuString,
    InvalidSudokuGrid
)
from tests.test_data.sudoku_grids import (
    ones, zeros, ones_3x9, ones_9x5, valid_rows, valid_cols, valid_boxes,
    grid1, grid2, grid2_result, difficult_case_grid, difficult_case_grid_result
)


@contextmanager
def does_not_raise():
    yield


@pytest.mark.parametrize('grid, result', [
    (ones, False),
    (zeros, True),
    (valid_rows, False),
    (valid_cols, True),
    (valid_boxes, False)
])
@pytest.mark.parametrize('col', [i for i in range(9)])
def test_is_valid_column(grid, col, result):
    assert is_valid_column(grid, col) is result


@pytest.mark.parametrize('grid, result', [
    (ones, False),
    (zeros, True),
    (valid_rows, True),
    (valid_cols, False),
    (valid_boxes, False)
])
@pytest.mark.parametrize('row', [i for i in range(9)])
def test_is_valid_row(grid, row, result):
    assert is_valid_row(grid, row) is result


@pytest.mark.parametrize('grid, result', [
    (ones, False),
    (zeros, True),
    (valid_rows, False),
    (valid_cols, False),
    (valid_boxes, True)
])
def test_is_valid_boxes(grid, result):
    assert is_valid_boxes(grid) is result


@pytest.mark.parametrize('grid, result', [
    (ones, False),
    (zeros, True),
    (valid_rows, False),
    (valid_cols, False),
    (valid_boxes, False)
])
def test_is_valid_sudoku_grid(grid, result):
    assert is_valid_sudoku_grid(grid) is result


@pytest.mark.parametrize('grid, sudoku_str, expectation', [
    (None, "1"*15, pytest.raises(InvalidSudokuString)),
    (zeros, "."*81, does_not_raise()),
    (zeros, "0"*81, does_not_raise()),
    (None, "zaq"*27, pytest.raises(InvalidSudokuString)),
    (valid_rows, "123456789"*9, does_not_raise()),
    (valid_boxes, "123123123456456456789789789"*3, does_not_raise()),
])
def test_sudoku_str_to_grid(grid, sudoku_str, expectation):
    with expectation:
        assert sudoku_str_to_grid(sudoku_str) == grid


@pytest.mark.parametrize('grid, sudoku_str, expectation', [
    (ones, "1"*81, does_not_raise()),
    (zeros, "."*81, does_not_raise()),
    (ones_3x9, "1"*27, pytest.raises(InvalidSudokuGrid)),
    (ones_9x5, "1"*45, pytest.raises(InvalidSudokuGrid)),
    (valid_rows, "123456789"*9, does_not_raise()),
    (valid_boxes, "123123123456456456789789789"*3, does_not_raise()),
])
def test_grid_to_sudoku_str(grid, sudoku_str, expectation):
    with expectation:
        assert grid_to_sudoku_str(grid) == sudoku_str


@pytest.mark.parametrize('grid, x, y, val, result', [
    (grid1, 0, 2, 3, False),
    (grid1, 2, 0, 7, True),
    (grid1, 2, 1, 7, True),
    (grid1, 2, 2, 7, False),
    (grid1, 0, 2, 4, True),
    (grid1, 0, 2, 4, True),
    (grid1, 1, 2, 4, True),
    (grid1, 2, 2, 4, False),
])
def test_is_safe(grid, x, y, val, result):
    assert is_safe(grid, x, y, val) == result


@pytest.mark.parametrize('sudoku_grid, result_grid, is_solved', [
    (grid2, grid2_result, True),
    (difficult_case_grid, difficult_case_grid_result, True)
])
def test_solving_sudoku_workflow(sudoku_grid, result_grid, is_solved):
    result = sudoku_grid.copy()
    assert solve_sudoku(result) == is_solved
    assert result == result_grid
