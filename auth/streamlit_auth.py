"""Streamlit-facing authentication facade.

The central auth flow lives in dashboards/app.py. This module remains as a
small compatibility layer for shared UI and older imports.
"""

from __future__ import annotations

from uuid import uuid4

import html
import streamlit as st

from auth.auth_guard import VALID_ROLES, is_valid_role, role_label
from auth.auth_service import authenticate_credentials, validate_token
from auth.session_manager import (
    clear_auth_session,
    current_user_context,
    init_anonymous_session,
    is_authenticated_session,
    restore_authenticated_session,
    start_authenticated_session,
)
from auth.token_manager import (
    clear_auth_cookie,
    create_session_token,
    get_stored_token,
    store_auth_token,
)


def clear_auth_cache():
    """Clear Streamlit caches that may contain stale auth-dependent data."""
    for cache in (getattr(st, "cache_data", None), getattr(st, "cache_resource", None)):
        clear = getattr(cache, "clear", None)
        if callable(clear):
            try:
                clear()
            except Exception:
                pass


def is_authenticated() -> bool:
    return is_authenticated_session() and is_valid_role(st.session_state.get("role"))


def invalidate_auth(cookies=None, *, clear_cache: bool = True, clear_all_session: bool = True) -> None:
    cleanup_error = None
    if cookies is not None:
        try:
            clear_auth_cookie(cookies)
        except Exception as exc:
            cleanup_error = exc
    
    if clear_cache:
        try:
            clear_auth_cache()
        except Exception as exc:
            if cleanup_error is None:
                cleanup_error = exc
    
    try:
        clear_auth_session(clear_all=clear_all_session)
    except Exception as exc:
        if cleanup_error is None:
            cleanup_error = exc

    if cleanup_error is not None:
        raise cleanup_error


def ensure_authenticated(cookies=None) -> bool:
    init_anonymous_session()

    # Local development: trust session state only
    if cookies is None:
        return is_authenticated()

    token = get_stored_token(cookies)
    if not token:
        return False

    if is_authenticated() and st.session_state.get("auth_token") == token:
        return True

    resolved = validate_token(token)
    if not resolved:
        invalidate_auth(cookies)
        return False

    user, payload = resolved
    restore_authenticated_session(user, token, str(payload["session_id"]))
    return True


def login_user(username: str, password: str, cookies=None) -> bool:
    user = authenticate_credentials(username, password)
    if not user:
        return False

    session_id = str(uuid4())
    token = create_session_token(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        role=user.role,
        session_id=session_id,
    )
    start_authenticated_session(user, token, session_id)
    # Cookie storage is optional in local development
    if cookies is not None:
        try:
            store_auth_token(cookies, token)
        except Exception:
            pass
    return True


def logout_user(cookies=None):
    try:
        invalidate_auth(cookies, clear_all_session=True)
    except Exception:
        pass
    finally:
        # Ensure cookie cleanup happens even if session cleanup raised
        if cookies is not None:
            try:
                clear_auth_cookie(cookies)
            except Exception:
                pass
        st.rerun()


def show_sidebar_user_profile(cookies=None):
    """Render the current authenticated user only."""
    if not is_authenticated():
        return

    user = current_user_context()
    username = html.escape(str(user.get("username") or "User"))
    email = html.escape(str(user.get("email") or ""))
    role = str(user.get("role") or "").lower()
    display_role = role_label(role)
    initials = "".join(part[:1] for part in username.split()[:2]).upper() or "U"

    badge_colors = {
        "admin": "#ef4444",
        "coach": "#3b82f6",
        "scout": "#10b981",
        "analyst": "#f59e0b",
    }
    badge_color = badge_colors.get(role, "#64748b")

    st.sidebar.markdown(
        f"""
        <style>
        .sporta-sidebar-user {{
            margin: 0.25rem 0 1rem;
            padding: 1rem;
            border-radius: 14px;
            border: 1px solid rgba(148, 163, 184, 0.22);
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.94), rgba(30, 41, 59, 0.94));
            box-shadow: 0 14px 35px rgba(2, 6, 23, 0.22);
        }}
        .sporta-sidebar-head {{ display: flex; align-items: center; gap: 0.75rem; }}
        .sporta-sidebar-avatar {{
            width: 42px; height: 42px; border-radius: 14px;
            display: grid; place-items: center;
            color: #f8fafc; background: #0ea5e9; font-weight: 850;
        }}
        .sporta-sidebar-name {{ color: #f8fafc; font-weight: 800; line-height: 1.2; overflow-wrap: anywhere; }}
        .sporta-sidebar-email {{ color: #94a3b8; font-size: 0.78rem; overflow-wrap: anywhere; margin-top: 0.15rem; }}
        .sporta-role-badge {{
            display: inline-flex; margin-top: 0.8rem; padding: 0.22rem 0.62rem;
            border-radius: 999px; color: white; background: {badge_color};
            font-size: 0.74rem; font-weight: 800; letter-spacing: 0;
        }}
        </style>
        <div class="sporta-sidebar-user">
            <div class="sporta-sidebar-head">
                <div class="sporta-sidebar-avatar">{html.escape(initials)}</div>
                <div>
                    <div class="sporta-sidebar-name">{username}</div>
                    <div class="sporta-sidebar-email">{email}</div>
                </div>
            </div>
            <div class="sporta-role-badge">{display_role}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.sidebar.button("Logout", use_container_width=True, type="secondary"):
        logout_user(cookies)


# Backward-compatible names used by older tests/imports.
authenticate_user = authenticate_credentials
resolve_user_from_token = lambda token: (validate_token(token) or (None, None))[0]
persist_auth_token = store_auth_token
init_auth_session_state = init_anonymous_session
set_auth_session = lambda user: start_authenticated_session(user, st.session_state.get("auth_token"), st.session_state.get("session_id"))
