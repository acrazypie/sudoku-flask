"""
Authentication routes for Google OAuth
"""

import os
import json
import base64
from flask import Blueprint, redirect, url_for, session, request
from flask_login import login_user, logout_user, current_user
from google_auth_oauthlib.flow import Flow
from google.oauth2.service_account import Credentials
from app.models import User, db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]


def _get_redirect_uri():
    """Get the redirect URI, handling both dev and production"""
    # Use environment variable if set, otherwise generate from current request
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI")
    if not redirect_uri:
        redirect_uri = url_for("auth.callback", _external=True)
    return redirect_uri


def _decode_jwt(token):
    """Decode JWT token without verification (for local dev)"""
    try:
        # JWT format: header.payload.signature
        parts = token.split(".")
        if len(parts) != 3:
            return None

        # Decode payload (add padding if needed)
        payload = parts[1]
        # Add padding
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += "=" * padding

        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except Exception as e:
        print(f"Error decoding JWT: {e}")
        return None


@auth_bp.route("/login")
def login():
    """Redirect user to Google login"""
    redirect_uri = _get_redirect_uri()

    # Create authorization request
    flow = Flow.from_client_config(
        client_config={
            "installed": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri],
            }
        },
        scopes=SCOPES,
        redirect_uri=redirect_uri,
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
    redirect_uri = _get_redirect_uri()
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
                "redirect_uris": [redirect_uri],
            }
        },
        scopes=SCOPES,
        state=state,
        redirect_uri=redirect_uri,
    )

    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    # Get user info from ID token (decode JWT)
    id_token = credentials.id_token
    id_token_decoded = _decode_jwt(id_token)

    if not id_token_decoded:
        return redirect(url_for("main.index"))

    # Parse ID token to get user info
    google_id = id_token_decoded.get("sub")
    email = id_token_decoded.get("email")
    name = id_token_decoded.get("name")
    picture = id_token_decoded.get("picture")

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
