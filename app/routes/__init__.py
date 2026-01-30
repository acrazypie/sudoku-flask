"""
Routes package for Sudoku Flask app
"""

from .main import main_bp
from .api import api_bp
from .auth import auth_bp

__all__ = ["main_bp", "api_bp", "auth_bp"]
