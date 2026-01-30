"""
Main page routes for Sudoku game
Handles rendering HTML templates
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import User, db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Serve the start screen"""
    return render_template("start.html")


@main_bp.route("/game")
def game():
    """Serve the game screen"""
    return render_template("game.html")


@main_bp.route("/over")
def over():
    """Serve the game over screen - only accessible if game was lost"""
    game_state = request.cookies.get("game_state")
    if game_state != "lost":
        return redirect(url_for("main.index"))
    return render_template("over.html")


@main_bp.route("/win")
def win():
    """Serve the win screen - only accessible if game was won"""
    game_state = request.cookies.get("game_state")
    if game_state != "won":
        return redirect(url_for("main.index"))
    return render_template("win.html")


@main_bp.route("/profile")
@login_required
def profile():
    """Serve the user profile page"""
    return render_template("profile.html", user=current_user)


@main_bp.route("/api/profile/update-nickname", methods=["POST"])
@login_required
def update_nickname():
    """Update user nickname"""
    data = request.get_json()
    nickname = data.get("nickname", "").strip()

    if not nickname or len(nickname) < 1 or len(nickname) > 50:
        return (
            jsonify({"success": False, "error": "Nickname must be 1-50 characters"}),
            400,
        )

    try:
        current_user.nickname = nickname
        db.session.commit()
        return jsonify({"success": True, "message": "Nickname updated successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
