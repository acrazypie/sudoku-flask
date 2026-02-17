"""
Constants for Sudoku board configuration.
"""

GRID_SIZE = 9
BOX_SIZE = 3
ALL_VALUES = set(range(1, GRID_SIZE + 1))
EMPTY_CELL = 0

BOX_INDICES = [
    [0, 1, 2, 9, 10, 11, 18, 19, 20],
    [3, 4, 5, 12, 13, 14, 21, 22, 23],
    [6, 7, 8, 15, 16, 17, 24, 25, 26],
    [27, 28, 29, 36, 37, 38, 45, 46, 47],
    [30, 31, 32, 39, 40, 41, 48, 49, 50],
    [33, 34, 35, 42, 43, 44, 51, 52, 53],
    [54, 55, 56, 63, 64, 65, 72, 73, 74],
    [57, 58, 59, 66, 67, 68, 75, 76, 77],
    [60, 61, 62, 69, 70, 71, 78, 79, 80],
]

ROW_INDICES = [list(range(i * 9, i * 9 + 9)) for i in range(9)]
COL_INDICES = [list(range(i, 81, 9)) for i in range(9)]


def get_box_indices(box_row: int, box_col: int) -> list:
    """Get cell indices for a specific box (0-indexed)."""
    start_row = box_row * 3
    start_col = box_col * 3
    return [
        r * 9 + c
        for r in range(start_row, start_row + 3)
        for c in range(start_col, start_col + 3)
    ]


def get_box_for_index(index: int) -> tuple:
    """Get box row and column for a given cell index."""
    row = index // 9
    col = index % 9
    return (row // 3, col // 3)


def get_row_for_index(index: int) -> int:
    """Get row number for a given cell index."""
    return index // 9


def get_col_for_index(index: int) -> int:
    """Get column number for a given cell index."""
    return index % 9
