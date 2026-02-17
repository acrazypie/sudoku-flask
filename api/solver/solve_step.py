"""
SolveStep represents a single solving action.
"""

from dataclasses import dataclass
from typing import List, Optional, Set


@dataclass
class SolveStep:
    """
    Represents a single step in solving a Sudoku puzzle.

    Attributes:
        technique: Name of the solving technique used
        cell_index: Index of the cell being modified
        value: Value placed (for single placement techniques)
        candidates_removed: Candidates removed from a cell
        affected_cells: Additional cells affected by this step
        explanation: Human-readable explanation
    """
    technique: str
    cell_index: int
    value: Optional[int] = None
    candidates_removed: Optional[Set[int]] = None
    affected_cells: Optional[List[int]] = None
    explanation: str = ""

    def __post_init__(self):
        if self.affected_cells is None:
            self.affected_cells = []
        if self.candidates_removed is None:
            self.candidates_removed = set()

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "technique": self.technique,
            "cell_index": self.cell_index,
            "value": self.value,
            "candidates_removed": list(self.candidates_removed) if self.candidates_removed else [],
            "affected_cells": self.affected_cells,
            "explanation": self.explanation,
        }
