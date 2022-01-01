class InvalidSudokuString(Exception):
    pass


class InvalidSudokuGrid(Exception):
    pass


def is_valid_column(grid, column_number):
    """
    Checks whether column is correct sudoku column. Column is valid when each
    value is different (zeros are omitted).

    Args:
        grid (list): Matrix with partially/fully filled-in sudoku.
        column_number (int): The column number.

    Returns:
        bool: Whether column is valid sudoku column or not.
    """
    column = list(filter(
        lambda value: value != 0, [row[column_number] for row in grid]
    ))
    return len(column) == len(set(column))


def is_valid_row(grid, row_num):
    """
    Checks whether row is correct sudoku row. Row is valid when each value is
    different (zeros are omitted).

    Args:
        grid (list): Matrix with partially/fully filled-in sudoku.
        row_num (int): The row number.

    Returns:
        bool: Whether row is valid sudoku row or not.
    """
    row = list(filter(lambda value: value != 0, grid[row_num]))
    return len(row) == len(set(row))


def is_valid_boxes(grid):
    """
    Checks whether all boxes are correct sudoku box. Box is valid when each
    value is different (zeros are omitted).

    Args:
        grid (list): Matrix with partially/fully filled-in sudoku.

    Returns:
        bool: Whether all boxes are valid sudoku box or not.
    """
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            box = []
            for x in range(row, row+3):
                for y in range(col, col+3):
                    if grid[x][y] != 0:
                        box.append(grid[x][y])
            if len(box) != len(set(box)):
                return False
    return True


def is_valid_sudoku_grid(grid):
    """
    Checks whether grid is correct sudoku grid. Grid is correct when each row
    is correct sudoku row, each column is correct sudoku column and each box is
    correct sudoku box.

    Args:
        grid (list): Matrix with partially/fully filled-in sudoku.

    Returns:
        bool: Whether passed grid is valid sudoku grid or not.
    """
    for i in range(9):
        is_valid = is_valid_row(grid, i)
        if not is_valid:
            return False
        is_valid = is_valid_column(grid, i)
        if not is_valid:
            return False
    return is_valid_boxes(grid)


def sudoku_str_to_grid(sudoku_str):
    """Convert sudoku string to sudoku grid (2D list).

    Args:
        sudoku_str (str): Sudoku grid as string which can only contains digits
            or dots(same as 0).

    Raises:
        InvalidSudokuString: String is too long or contains disallowed
            characters.
    """
    if len(sudoku_str) != 81:
        raise InvalidSudokuString('Too many characters!')

    # Characters validation
    for letter in sudoku_str:
        if not letter.isdecimal() and letter != '.':
            raise InvalidSudokuString(f'{letter} is not a decimal or "." !')

    sudoku_str = sudoku_str.replace('.', '0')
    grid = [[] for _ in range(9)]
    for i, letter in enumerate(sudoku_str):
        grid[i // 9].append(int(letter))
    return grid


def grid_to_sudoku_str(grid):
    """Convert sudoku grid (2D list) to sudoku string.

    Args:
        grid (list): 2D list  (9x9) as representation of sudoku grid.

    Raises:
        InvalidSudokuGrid: When grid has got wrong dimension.

    Returns:
        str: Sudoku grid as string which can only contains digits or dots (same
            as 0).
    """
    if len(grid) != 9:
        raise InvalidSudokuGrid('Wrong dimension of sudoku matrix!')
    for row in grid:
        if len(row) != 9:
            raise InvalidSudokuGrid('Wrong dimension of sudoku matrix!')
    return ''.join(
        str(digit) if digit != 0 else '.' for row in grid for digit in row
    )


def is_safe(grid, row, column, number):
    """
    Checks whether it will be legal to assign number to the given row & column.

    Args:
        grid (list): Matrix with partially filled-in sudoku.
        row (int): Row index.
        column (int): Column index.
        number (int): Assignation value.

    Returns:
        bool: Whether assignation is legal or not.
    """
    # Checking row
    for x in range(9):
        if grid[row][x] == number:
            return False

    # Checking column
    for x in range(9):
        if grid[x][column] == number:
            return False

    # Checking box
    start_row = row - row % 3
    start_column = column - column % 3
    for x in range(3):
        for y in range(3):
            if grid[x + start_row][y + start_column] == number:
                return False
    return True


def solve_sudoku(grid, row=0, column=0):
    """
    Takes a partially filled-in grid and attempt to assign values to all
    unassigned locations in such a way to meet the requirements for Sudoku
    solution (non-duplication across rows, columns, and boxes)

    Args:
            grid (list): Partially filled-in sudoku grid.
            row (int): Row index. Defaults to 0.
            column (int): Column index. Defaults to 0.

    Returns:
            bool: If sudoku can be solved or not. Solution in `grid` if exists.
    """
    # Avoid further backtracking
    if (row == 8 and column == 9):
        return True

    # Go to next row of grid
    if column == 9:
        row += 1
        column = 0

    # Skip cell if it contains value (go to next step)
    if grid[row][column] > 0:
        return solve_sudoku(grid, row, column + 1)

    for number in range(1, 10):
        # Check if `number` can be assigned in `row` & `column`. Move to next
        # column if `number` can be inserted.
        if is_safe(grid, row, column, number):
            grid[row][column] = number
            if solve_sudoku(grid, row, column + 1):
                return True

        # Assumption went wrong, reset value and go to next assumption with
        # different `number` value
        grid[row][column] = 0
    return False
