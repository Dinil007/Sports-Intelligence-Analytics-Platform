"""Streamlit session lifecycle helpers for authentication."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import streamlit as st

from auth.auth_service import AuthenticatedUser

AUTH_SESSION_KEYS = (
    "authenticated",
    "user_id",
    "username",
    "email",
    "role",
    "login_timestamp",
    "session_id",
    "auth_token",
)


INTERNAL_AUTH_KEYS = (
    "_page_registry",
    "_auth_cookie_ready_attempts",
    "_auth_storage_unavailable",
    "_auth_error",
)


def init_anonymous_session() -> None:
    for key, value in [
        ("authenticated", False),
        ("user_id", None),
        ("username", None),
        ("email", None),
        ("role", None),
        ("login_timestamp", None),
        ("session_id", None),
        ("auth_token", None),
    ]:
        try:
            st.session_state.setdefault(key, value)
        except Exception:
            pass


def _should_preserve_session_key(key: str, *, preserve_cookie_manager: bool) -> bool:
    key_str = str(key)
    key_lower = key_str.lower()
    
    if preserve_cookie_manager:
        if key_str.startswith("CookieManager.") or "cookie" in key_lower:
            return True
            
    # Keep theme settings and configuration intact.
    if "theme" in key_lower or "config" in key_lower:
        return True
        
    # Keep Streamlit's own internals intact; they are not application auth state.
    if key_str.startswith("$$"):
        return True
        
    if key_str.startswith("_"):
        # Clear specific internal auth keys, preserve other internal/system keys
        if key_str in INTERNAL_AUTH_KEYS:
            return False
        return True
        
    return False


def _delete_session_key(key: str) -> None:
    try:
        if key in st.session_state:
            del st.session_state[key]
    except Exception:
        pass


def clear_all_session_state(*, preserve_cookie_manager: bool = False) -> None:
    """Clear app-owned session state without reassigning component keys.

    Streamlit can reject writes to widget/component-backed keys after a widget is
    instantiated. Deleting only non-preserved keys avoids the unsafe pattern of
    clear-then-restore, while still removing all auth and app state.
    """
    keys = list(st.session_state.keys())
    for key in keys:
        if _should_preserve_session_key(key, preserve_cookie_manager=preserve_cookie_manager):
            continue
        _delete_session_key(key)


def clear_application_session_state() -> None:
    clear_all_session_state(preserve_cookie_manager=True)


def clear_auth_session(*, clear_all: bool = False) -> None:
    try:
        if clear_all:
            clear_all_session_state(preserve_cookie_manager=True)
        else:
            for key in AUTH_SESSION_KEYS + INTERNAL_AUTH_KEYS:
                _delete_session_key(key)
    finally:
        init_anonymous_session()


def start_authenticated_session(user: AuthenticatedUser, token: str, session_id: str | None = None) -> None:
    clear_application_session_state()
    fresh_session_id = session_id or str(uuid4())
    
    for key, val in [
        ("authenticated", True),
        ("user_id", user.user_id),
        ("username", user.username),
        ("email", user.email),
        ("role", user.role),
        ("login_timestamp", datetime.now(timezone.utc).isoformat()),
        ("session_id", fresh_session_id),
        ("auth_token", token),
    ]:
        try:
            st.session_state[key] = val
        except Exception:
            pass


def restore_authenticated_session(user: AuthenticatedUser, token: str, session_id: str) -> None:
    clear_auth_session(clear_all=False)
    
    for key, val in [
        ("authenticated", True),
        ("user_id", user.user_id),
        ("username", user.username),
        ("email", user.email),
        ("role", user.role),
        ("login_timestamp", datetime.now(timezone.utc).isoformat()),
        ("session_id", session_id),
        ("auth_token", token),
    ]:
        try:
            st.session_state[key] = val
        except Exception:
            pass


def is_authenticated_session() -> bool:
    return bool(
        st.session_state.get("authenticated")
        and st.session_state.get("user_id") is not None
        and st.session_state.get("username")
        and st.session_state.get("role")
        and st.session_state.get("session_id")
        and st.session_state.get("auth_token")
    )


def current_user_context() -> dict:
    return {
        "user_id": st.session_state.get("user_id"),
        "username": st.session_state.get("username"),
        "email": st.session_state.get("email"),
        "role": st.session_state.get("role"),
        "session_id": st.session_state.get("session_id"),
    }
