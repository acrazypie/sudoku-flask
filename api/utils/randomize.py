"""
Randomization utilities.
"""

import random
from typing import Optional


def shuffle_list(lst: list) -> list:
    """Shuffle and return a copy of a list."""
    result = lst.copy()
    random.shuffle(result)
    return result


def random_value(exclude: Optional[set] = None) -> Optional[int]:
    """Get a random value 1-9, excluding given values."""
    if exclude is None:
        exclude = set()
    available = [v for v in range(1, 10) if v not in exclude]
    return random.choice(available) if available else None
