"""
API routes for Sudoku game
Handles puzzle generation, solving, validation, and scoring
"""

from flask import Blueprint, jsonify, request, session

from api.generator.puzzle_generator import PuzzleGenerator
from api.solver.solver import SudokuSolver
from api.hints.hint_engine import HintEngine
from api.board.board import Board
from api.board.constants import EMPTY_CELL
from api.validation.rules import validate_complete

api_bp = Blueprint("api", __name__, url_prefix="/api")

_generator = PuzzleGenerator()
_solver = SudokuSolver()
_hint_engine = HintEngine()


def _board_to_string(board: Board) -> str:
    """Convert board to string representation."""
    result = []
    for i in range(81):
        val = board.get_cell_by_index(i).value
        result.append(str(val) if val != EMPTY_CELL else ".")
    return "".join(result)


def _string_to_board(board_str: str) -> Board:
    """Convert string to board."""
    values = []
    for char in board_str:
        if char == ".":
            values.append(EMPTY_CELL)
        else:
            values.append(int(char))
    return Board(values)


@api_bp.route("/generate", methods=["POST"])
def generate_puzzle():
    """Generate a new Sudoku puzzle based on difficulty"""
    data = request.get_json() or {}
    difficulty = data.get("difficulty", "easy")

    try:
        puzzle_board = _generator.generate(difficulty)
        
        puzzle_str = _board_to_string(puzzle_board)
        
        solution_board = puzzle_board.copy()
        _solver.solve(solution_board, collect_steps=False)
        solution_str = _board_to_string(solution_board)

        session["puzzle"] = puzzle_str
        session["solution"] = solution_str
        session["difficulty"] = difficulty

        return jsonify({"success": True, "puzzle": puzzle_str, "difficulty": difficulty})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@api_bp.route("/solve", methods=["POST"])
def solve_puzzle():
    """Solve a given Sudoku puzzle"""
    data = request.get_json()
    board_str = data.get("board", "")

    try:
        board = _string_to_board(board_str)
        solved = board.copy()
        _solver.solve(solved, collect_steps=False)
        solution_str = _board_to_string(solved)
        return jsonify({"success": True, "solution": solution_str})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@api_bp.route("/validate", methods=["POST"])
def validate_move():
    """Validate if a move is correct"""
    data = request.get_json()
    board_str = data.get("board", "")
    index = data.get("index", -1)
    value = data.get("value", "")
    solution = data.get("solution", "")

    try:
        if 0 <= index < 81 and solution and index < len(solution):
            is_correct = solution[index] == value
            return jsonify({"success": True, "correct": is_correct})
        return jsonify({"success": False, "error": "Invalid index or solution"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@api_bp.route("/get-hint", methods=["POST"])
def get_hint():
    """Get a hint for the current board"""
    data = request.get_json()
    board_str = data.get("board", "")
    solution_str = data.get("solution", "")

    try:
        if not solution_str or not board_str:
            return (
                jsonify({"success": False, "error": "Missing board or solution"}),
                400,
            )

        board = _string_to_board(board_str)
        
        _hint_engine.reset()
        step = _hint_engine.get_next_hint(board)
        
        if step and step.value is not None:
            index = step.cell_index
            value = str(step.value)
            return jsonify({
                "success": True, 
                "index": index, 
                "value": value,
                "explanation": step.explanation
            })

        return jsonify({"success": False, "error": "No hints available"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@api_bp.route("/score", methods=["POST"])
def save_score():
    """
    Save game score to session.

    Expected JSON:
    {
        "difficulty": "easy|medium|expert|master|extreme",
        "time": <seconds>,
        "mistakes": <number>,
        "score": <calculated score>
    }
    """
    data = request.get_json() or {}

    try:
        if "scores" not in session:
            session["scores"] = []

        score_entry = {
            "difficulty": data.get("difficulty", "unknown"),
            "time": data.get("time", 0),
            "mistakes": data.get("mistakes", 0),
            "score": data.get("score", 0),
            "timestamp": data.get("timestamp", ""),
        }

        session["scores"].append(score_entry)
        session.modified = True

        scores_list = [s["score"] for s in session["scores"]]
        stats = {
            "current_score": score_entry["score"],
            "total_games": len(session["scores"]),
            "highest_score": max(scores_list) if scores_list else 0,
            "average_score": sum(scores_list) / len(scores_list) if scores_list else 0,
            "all_scores": session["scores"],
        }

        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
