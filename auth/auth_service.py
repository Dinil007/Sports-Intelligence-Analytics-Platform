"""Database-backed authentication service."""

from __future__ import annotations

from dataclasses import dataclass

from auth.auth_guard import normalize_role
from auth.models import User
from auth.security import verify_password
from auth.token_manager import decode_session_token
from database.db_connection import SessionLocal


@dataclass(frozen=True)
class AuthenticatedUser:
    user_id: int
    username: str
    email: str
    role: str


def sanitize_username(username: str | None) -> str:
    return str(username or "").strip()


def _to_authenticated_user(user: User) -> AuthenticatedUser | None:
    role = normalize_role(user.role)
    if not role:
        return None
    return AuthenticatedUser(
        user_id=int(user.id),
        username=str(user.username),
        email=str(user.email),
        role=role,
    )


def authenticate_credentials(username: str, password: str) -> AuthenticatedUser | None:
    clean_username = sanitize_username(username)
    if not clean_username or not password:
        return None

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == clean_username).first()
        if not user or not verify_password(str(password), user.password_hash):
            return None
        auth_user = _to_authenticated_user(user)
        return auth_user
    finally:
        db.close()


def get_user_by_username(username: str) -> AuthenticatedUser | None:
    clean_username = sanitize_username(username)
    if not clean_username:
        return None

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == clean_username).first()
        return _to_authenticated_user(user) if user else None
    finally:
        db.close()


def validate_token(token: str | None) -> tuple[AuthenticatedUser, dict] | None:
    payload = decode_session_token(token)
    if not payload:
        return None

    username = sanitize_username(payload.get("sub"))
    token_role = normalize_role(payload.get("role"))
    token_user_id = payload.get("user_id")
    if not username or not token_role or token_user_id is None:
        return None

    user = get_user_by_username(username)
    if not user:
        return None

    try:
        user_id_matches = int(token_user_id) == user.user_id
    except (TypeError, ValueError):
        return None

    if not user_id_matches:
        return None
    if token_role != user.role:
        return None

    return user, payload
