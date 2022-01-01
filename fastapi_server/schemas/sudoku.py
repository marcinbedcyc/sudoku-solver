from pydantic import BaseModel, Field


class SudokuBase(BaseModel):
    sudoku: str = Field(
        ...,
        max_length=81,
        min_length=81,
        example=(
            '..98..7.41..5..6...3...7.9.5.27.8.3..81.5...664.123.5....24.3..9.'
            '.6.18....5..9.2.'
        ),
        title='Sudoku\'s string',
        description=(
            'The string of sudoku with length equals 81 and it only contains '
            'digits and dot character (dot is treated same as 0).'
        ),
        regex=r'^[\d\.]+$'  # Only digits and dot character are allowed
    )


class SudokuIn(SudokuBase):
    pass


class SudokuOut(SudokuBase):
    solvable: bool = Field(
        ...,
        title='If sudoku is solvable',
        description=(
            'Whether sudoku is solvable or not. It depends on the  correctness'
            ' of the sent sudoku\'s string.'
        )
    )
