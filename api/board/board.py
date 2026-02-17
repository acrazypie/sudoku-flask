"""
Board class representing a 9x9 Sudoku grid.
"""

from typing import List, Optional, Set
from .cell import Cell
from .constants import (
    GRID_SIZE, EMPTY_CELL, ALL_VALUES,
    ROW_INDICES, COL_INDICES, BOX_INDICES, get_box_for_index
)


class Board:
    """Represents a 9x9 Sudoku board."""

    def __init__(self, initial_values: Optional[List[int]] = None):
        """
        Initialize a new board.

        Args:
            initial_values: Optional list of 81 integers (0 for empty)
        """
        self._cells: List[Cell] = [Cell() for _ in range(GRID_SIZE * GRID_SIZE)]
        if initial_values:
            self._initialize_from_list(initial_values)

    def _initialize_from_list(self, values: List[int]) -> None:
        """Initialize board from a list of 81 values."""
        for i, val in enumerate(values):
            if val != EMPTY_CELL:
                self._cells[i] = Cell(val, fixed=True)

    @property
    def cells(self) -> List[Cell]:
        """Get the list of cells."""
        return self._cells

    def get_cell(self, row: int, col: int) -> Cell:
        """Get cell at row and column (0-indexed)."""
        return self._cells[row * 9 + col]

    def get_cell_by_index(self, index: int) -> Cell:
        """Get cell at linear index (0-80)."""
        return self._cells[index]

    def set_value(self, row: int, col: int, value: int, fixed: bool = False) -> None:
        """Set a cell value."""
        index = row * 9 + col
        self._cells[index] = Cell(value, fixed)

    def get_value(self, row: int, col: int) -> int:
        """Get cell value at row and column."""
        return self._cells[row * 9 + col].value

    def is_fixed(self, row: int, col: int) -> bool:
        """Check if cell is fixed."""
        return self._cells[row * 9 + col].fixed

    def get_candidates(self, row: int, col: int) -> Set[int]:
        """Get candidates for a cell."""
        return self._cells[row * 9 + col].candidates

    def get_row_values(self, row: int) -> Set[int]:
        """Get all values in a row."""
        values = set()
        for col in range(GRID_SIZE):
            val = self.get_value(row, col)
            if val != EMPTY_CELL:
                values.add(val)
        return values

    def get_col_values(self, col: int) -> Set[int]:
        """Get all values in a column."""
        values = set()
        for row in range(GRID_SIZE):
            val = self.get_value(row, col)
            if val != EMPTY_CELL:
                values.add(val)
        return values

    def get_box_values(self, box_row: int, box_col: int) -> Set[int]:
        """Get all values in a 3x3 box."""
        values = set()
        for idx in BOX_INDICES[box_row * 3 + box_col]:
            val = self._cells[idx].value
            if val != EMPTY_CELL:
                values.add(val)
        return values

    def get_box_for_cell(self, row: int, col: int) -> tuple:
        """Get box coordinates for a cell."""
        return get_box_for_index(row * 9 + col)

    def get_row_indices(self, row: int) -> List[int]:
        """Get all cell indices in a row."""
        return ROW_INDICES[row]

    def get_col_indices(self, col: int) -> List[int]:
        """Get all cell indices in a column."""
        return COL_INDICES[col]

    def get_box_indices(self, box_row: int, box_col: int) -> List[int]:
        """Get all cell indices in a box."""
        return BOX_INDICES[box_row * 3 + box_col]

    def get_related_indices(self, index: int) -> Set[int]:
        """Get all indices related to a cell (same row, col, box)."""
        row = index // 9
        col = index % 9
        box_row, box_col = get_box_for_index(index)

        related = set()
        related.update(ROW_INDICES[row])
        related.update(COL_INDICES[box_col * 9 + col])
        related.update(BOX_INDICES[box_row * 3 + box_col])
        related.discard(index)
        return related

    def get_empty_cells(self) -> List[int]:
        """Get indices of all empty cells."""
        return [i for i, cell in enumerate(self._cells) if cell.is_empty]

    def get_filled_cells(self) -> List[int]:
        """Get indices of all filled cells."""
        return [i for i, cell in enumerate(self._cells) if cell.is_solved]

    def count_filled(self) -> int:
        """Count number of filled cells."""
        return sum(1 for cell in self._cells if cell.is_solved)

    def count_empty(self) -> int:
        """Count number of empty cells."""
        return sum(1 for cell in self._cells if cell.is_empty)

    def is_complete(self) -> bool:
        """Check if the board is completely filled."""
        return all(cell.is_solved for cell in self._cells)

    def is_valid(self) -> bool:
        """Check if the board is valid (no rule violations)."""
        for row in range(GRID_SIZE):
            if not self._is_group_valid(ROW_INDICES[row]):
                return False
        for col in range(GRID_SIZE):
            if not self._is_group_valid(COL_INDICES[col]):
                return False
        for box in range(9):
            if not self._is_group_valid(BOX_INDICES[box]):
                return False
        return True

    def _is_group_valid(self, indices: List[int]) -> bool:
        """Check if a group (row, col, box) has no duplicates."""
        values = []
        for idx in indices:
            val = self._cells[idx].value
            if val != EMPTY_CELL:
                if val in values:
                    return False
                values.append(val)
        return True

    def to_list(self) -> List[int]:
        """Convert board to list of 81 integers."""
        return [cell.value for cell in self._cells]

    def to_display_string(self) -> str:
        """Get a string representation of the board."""
        lines = []
        for row in range(GRID_SIZE):
            row_vals = []
            for col in range(GRID_SIZE):
                val = self.get_value(row, col)
                if val == EMPTY_CELL:
                    row_vals.append(".")
                else:
                    row_vals.append(str(val))
            lines.append(" ".join(row_vals))
            if row % 3 == 2 and row < 8:
                lines.append("")
        return "\n".join(lines)

    def copy(self) -> 'Board':
        """Create a deep copy of the board."""
        new_board = Board()
        new_board._cells = [cell.copy() for cell in self._cells]
        return new_board

    def __repr__(self) -> str:
        return f"Board({self.to_list()})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return False
        return self.to_list() == other.to_list()
