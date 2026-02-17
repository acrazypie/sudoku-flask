# Sudoku Engine

A pure Python 3 Sudoku engine for generating, solving, and analyzing Sudoku puzzles.

## Features

- **Board Model**: Complete 9x9 grid with cell-level tracking of candidates
- **Puzzle Generator**: Generates valid Sudoku puzzles with unique solutions
- **Logical Solver**: Human-style solver using various techniques
- **Solving Techniques**:
  - Naked Single
  - Hidden Single
  - Naked Pair
  - Hidden Pair
  - Pointing Pair
- **Difficulty Analysis**: Rates puzzles based on required techniques
- **Hint Engine**: Provides progressive hints without modifying the board
- **Validation**: Rules checking and consistency validation

## Installation

```bash
pip install -e .
```

## Usage

### Generate a Puzzle

```python
from sudoku.generator.puzzle_generator import PuzzleGenerator
from sudoku.utils.formatting import format_board

generator = PuzzleGenerator()
puzzle = generator.generate(difficulty="medium")
print(format_board(puzzle))
```

### Solve Logically

```python
from sudoku.generator.puzzle_generator import PuzzleGenerator
from sudoku.solver.solver import SudokuSolver
from sudoku.utils.formatting import format_board

puzzle = PuzzleGenerator().generate(difficulty="medium")
solver = SudokuSolver()
solved = solver.solve(puzzle)
print(format_board(puzzle))
```

### Get Hints

```python
from sudoku.generator.puzzle_generator import PuzzleGenerator
from sudoku.hints.hint_engine import HintEngine

puzzle = PuzzleGenerator().generate(difficulty="medium")
hint_engine = HintEngine()
hint = hint_engine.get_next_hint(puzzle)
print(hint.explanation)
```

### Analyze Difficulty

```python
from sudoku.generator.puzzle_generator import PuzzleGenerator
from sudoku.difficulty.analyzer import DifficultyAnalyzer

puzzle = PuzzleGenerator().generate(difficulty="medium")
analyzer = DifficultyAnalyzer()
details = analyzer.get_details(puzzle)
print(details)
```

## Project Structure

```
sudoku/
├── board/          # Board and cell models
├── generator/     # Puzzle generation
├── solver/        # Logical solving engine
│   └── techniques/  # Individual solving techniques
├── difficulty/   # Difficulty analysis
├── hints/        # Hint generation
├── validation/  # Board validation
└── utils/       # Utility functions
```

## Requirements

- Python 3.9+

## License

MIT
