"""
Authentication routes for Google OAuth
"""

import os
from flask import Blueprint, redirect, url_for, session, request
from flask_login import login_user, logout_user, current_user
from google_auth_oauthlib.flow import Flow
from google.oauth2.service_account import Credentials
from app.models import User, db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
SCOPES = ["profile", "email"]


@auth_bp.route("/login")
def login():
    """Redirect user to Google login"""
    # Create authorization request
    flow = Flow.from_client_config(
        client_config={
            "installed": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [url_for("auth.callback", _external=True)],
            }
        },
        scopes=SCOPES,
        redirect_uri=url_for("auth.callback", _external=True),
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
    )

    session["state"] = state
    return redirect(authorization_url)


@auth_bp.route("/callback")
def callback():
    """Handle Google OAuth callback"""
    state = session.get("state")
    authorization_response = request.url

    # Exchange authorization code for access token
    flow = Flow.from_client_config(
        client_config={
            "installed": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [url_for("auth.callback", _external=True)],
            }
        },
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for("auth.callback", _external=True),
    )

    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    # Get user info from ID token
    id_token = credentials.id_token

    # Parse ID token to get user info
    google_id = id_token.get("sub")
    email = id_token.get("email")
    name = id_token.get("name")
    picture = id_token.get("picture")

    # Find or create user
    user = User.query.filter_by(google_id=google_id).first()

    if not user:
        user = User(
            google_id=google_id,
            email=email,
            name=name,
            picture=picture,
            nickname=name.split()[0] if name else "User",
        )
        db.session.add(user)
        db.session.commit()

    # Log the user in
    login_user(user)

    return redirect(url_for("main.index"))


@auth_bp.route("/logout")
def logout():
    """Log out the current user"""
    logout_user()
    session.clear()
    return redirect(url_for("main.index"))
