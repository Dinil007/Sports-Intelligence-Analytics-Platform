"""JWT and browser cookie token management for Streamlit authentication."""

from __future__ import annotations

from auth.security import AUTH_COOKIE_KEY, create_access_token, decode_access_token

EMPTY_COOKIE_VALUES = frozenset({"", "{}", "null", '""', "None"})


def create_session_token(*, user_id: int, username: str, email: str, role: str, session_id: str) -> str:
    return create_access_token(
        {
            "sub": str(username),
            "user_id": int(user_id),
            "email": str(email),
            "role": str(role).lower(),
            "session_id": str(session_id),
        }
    )


def decode_session_token(token: str | None) -> dict | None:
    payload = decode_access_token(token)
    if not payload:
        return None
    if not payload.get("sub") or not payload.get("session_id"):
        return None
    return payload


def get_stored_token(cookies) -> str | None:
    try:
        token = cookies.get(AUTH_COOKIE_KEY)
    except Exception:
        return None
    if token is None:
        return None
    token = str(token).strip()
    if not token or token in EMPTY_COOKIE_VALUES:
        return None
    return token


def store_auth_token(cookies, token: str) -> None:
    cookies[AUTH_COOKIE_KEY] = token
    cookies.save()


def clear_auth_cookie(cookies) -> None:
    try:
        cookies[AUTH_COOKIE_KEY] = ""
        try:
            del cookies[AUTH_COOKIE_KEY]
        except Exception:
            pass
        cookies.save()
    except Exception:
        pass
