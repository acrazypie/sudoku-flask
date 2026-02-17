"""
Difficulty levels for Sudoku puzzles.
"""

from enum import Enum


class DifficultyLevel(Enum):
    """Enumeration of Sudoku difficulty levels."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"

    def __str__(self) -> str:
        return self.value


DIFFICULTY_CRITERIA = {
    "easy": {
        "max_technique_difficulty": 2,
        "max_steps": 50,
    },
    "medium": {
        "max_technique_difficulty": 3,
        "max_steps": 100,
    },
    "hard": {
        "max_technique_difficulty": 4,
        "max_steps": 200,
    },
    "expert": {
        "max_technique_difficulty": 5,
        "max_steps": 500,
    },
}


TECHNIQUE_DIFFICULTY = {
    "Naked Single": 1,
    "Hidden Single": 2,
    "Naked Pair": 3,
    "Hidden Pair": 4,
    "Pointing Pair": 4,
}
