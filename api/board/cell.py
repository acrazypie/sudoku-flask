"""
Cell class representing a single Sudoku cell.
"""

from .constants import EMPTY_CELL, ALL_VALUES


class Cell:
    """Represents a single cell in a Sudoku board."""

    def __init__(self, value: int = EMPTY_CELL, fixed: bool = False):
        """
        Initialize a cell.

        Args:
            value: The cell's value (0-9, where 0 is empty)
            fixed: Whether the cell is a fixed clue (cannot be changed)
        """
        self._value = value
        self._fixed = fixed
        self._candidates = set() if value != EMPTY_CELL else set(ALL_VALUES)

    @property
    def value(self) -> int:
        """Get the cell's value."""
        return self._value

    @value.setter
    def value(self, val: int) -> None:
        """Set the cell's value."""
        self._value = val
        if val == EMPTY_CELL:
            self._candidates = set(ALL_VALUES)
        else:
            self._candidates = set()

    @property
    def fixed(self) -> bool:
        """Check if the cell is fixed (clue)."""
        return self._fixed

    @fixed.setter
    def fixed(self, val: bool) -> None:
        """Set the fixed flag."""
        self._fixed = val

    @property
    def candidates(self) -> set:
        """Get the set of possible values for this cell."""
        return self._candidates.copy()

    @candidates.setter
    def candidates(self, val: set) -> None:
        """Set the candidates directly (used by solver)."""
        self._candidates = val

    @property
    def is_empty(self) -> bool:
        """Check if the cell is empty."""
        return self._value == EMPTY_CELL

    @property
    def is_solved(self) -> bool:
        """Check if the cell has a definitive value."""
        return self._value != EMPTY_CELL

    def remove_candidate(self, value: int) -> bool:
        """
        Remove a candidate from this cell.

        Returns:
            True if candidate was removed, False if not present
        """
        if value in self._candidates:
            self._candidates.discard(value)
            return True
        return False

    def set_value(self, value: int) -> None:
        """Set value and clear candidates."""
        self._value = value
        self._candidates = set()

    def clear(self) -> None:
        """Clear the cell value (make it empty)."""
        self._value = EMPTY_CELL
        self._candidates = set(ALL_VALUES)

    def copy(self) -> 'Cell':
        """Create a deep copy of this cell."""
        new_cell = Cell(self._value, self._fixed)
        new_cell._candidates = self._candidates.copy()
        return new_cell

    def __repr__(self) -> str:
        if self._value != EMPTY_CELL:
            return f"Cell({self._value}, fixed={self._fixed})"
        return f"Cell(candidates={sorted(self._candidates)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cell):
            return False
        return (
            self._value == other._value
            and self._fixed == other._fixed
            and self._candidates == other._candidates
        )
