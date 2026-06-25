import os
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

from auth.auth_guard import is_valid_role
from auth.navigation import PAGE_DEFINITIONS, ROLE_PAGE_KEYS
from auth.session_manager import clear_auth_session, init_anonymous_session
from auth.streamlit_auth import (
    ensure_authenticated,
    is_authenticated,
    login_user,
    logout_user,
    show_sidebar_user_profile,
)

st.set_page_config(
    page_title="SPORTA VISTA PRO",
    page_icon="\u26bd",
    layout="wide",
    initial_sidebar_state="expanded",
)

cookies = EncryptedCookieManager(
    prefix="sporta_app/",
    password=os.environ.get(
        "COOKIE_PASSWORD",
        "sporta-vista-pro-cookie-encryption-secret-key-32-chars",
    ),
)

COOKIE_READY_MAX_ATTEMPTS = 30
COOKIE_READY_RETRY_SECONDS = 0.1


def _restore_screen() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"], [data-testid="stHeader"], section.main {
            visibility: hidden !important;
        }
        </style>
        <div style="
            min-height: 80vh; display: flex; align-items: center; justify-content: center;
            color: #94a3b8; font-family: Inter, sans-serif; font-size: 1rem;
        ">Restoring session...</div>
        """,
        unsafe_allow_html=True,
    )


def _cookies_ready() -> bool:
    if cookies.ready():
        st.session_state.pop("_auth_cookie_ready_attempts", None)
        st.session_state.pop("_auth_storage_unavailable", None)
        return True

    attempts = int(st.session_state.get("_auth_cookie_ready_attempts", 0))
    if attempts >= COOKIE_READY_MAX_ATTEMPTS:
        st.session_state.pop("_auth_cookie_ready_attempts", None)
        st.session_state["_auth_storage_unavailable"] = True
        return False

    st.session_state["_auth_cookie_ready_attempts"] = attempts + 1
    _restore_screen()
    time.sleep(COOKIE_READY_RETRY_SECONDS)
    st.rerun()


def _restore_authentication() -> None:
    init_anonymous_session()
    if _cookies_ready():
        ensure_authenticated(cookies)
        return

    clear_auth_session(clear_all=True)
    st.session_state["_auth_storage_unavailable"] = True


_restore_authentication()


def _build_page_registry():
    registry = {}
    for key, (path, title, icon) in PAGE_DEFINITIONS.items():
        registry[key] = st.Page(path, title=title, icon=icon, default=(key == "home"))
    return registry


def _get_page_registry():
    if "_page_registry" not in st.session_state:
        st.session_state._page_registry = _build_page_registry()
    return st.session_state._page_registry


def _pages_for_role(role: str):
    registry = _get_page_registry()
    return [registry[key] for key in ROLE_PAGE_KEYS.get(role, [])]


def _login_styles() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] { display: none !important; }
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at top left, rgba(14, 165, 233, 0.20), transparent 34rem),
                linear-gradient(135deg, #020617 0%, #0f172a 46%, #111827 100%) !important;
        }
        .block-container {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }
        [data-testid="stForm"] {
            width: min(100%, 480px);
            background: rgba(15, 23, 42, 0.92) !important;
            border: 1px solid rgba(148, 163, 184, 0.24) !important;
            border-radius: 22px !important;
            padding: 2.25rem !important;
            box-shadow: 0 28px 80px rgba(2, 6, 23, 0.48) !important;
            backdrop-filter: blur(18px);
        }
        [data-testid="stTextInput"] label,
        [data-testid="stCheckbox"] label { color: #cbd5e1 !important; font-weight: 650 !important; }
        [data-testid="stTextInput"] input {
            border-radius: 12px !important;
            border: 1px solid rgba(148, 163, 184, 0.28) !important;
            background: rgba(2, 6, 23, 0.55) !important;
            color: #f8fafc !important;
            min-height: 2.8rem;
        }
        [data-testid="stTextInput"] input:focus {
            border-color: #38bdf8 !important;
            box-shadow: 0 0 0 1px #38bdf8 !important;
        }
        [data-testid="stFormSubmitButton"] button {
            min-height: 2.9rem;
            border-radius: 12px !important;
            border: 0 !important;
            background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
            color: white !important;
            font-weight: 850 !important;
        }
        .login-shell { width: min(100%, 520px); }
        .login-kicker {
            color: #38bdf8; font-size: 0.78rem; font-weight: 850;
            text-transform: uppercase; letter-spacing: 0.08em; text-align: center;
        }
        .login-title {
            margin: 0.35rem 0 0.4rem; color: #f8fafc; text-align: center;
            font-size: clamp(2rem, 6vw, 2.75rem); line-height: 1.02; font-weight: 950;
            letter-spacing: 0;
        }
        .login-subtitle {
            margin: 0 auto 1.8rem; color: #94a3b8; text-align: center;
            max-width: 24rem; font-size: 0.98rem; line-height: 1.55;
        }
        .login-meta {
            display: flex; gap: 0.55rem; justify-content: center; flex-wrap: wrap;
            margin-bottom: 1.5rem;
        }
        .login-pill {
            color: #cbd5e1; background: rgba(15, 23, 42, 0.86);
            border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 999px;
            padding: 0.32rem 0.68rem; font-size: 0.74rem; font-weight: 700;
        }
        @media (max-width: 560px) {
            [data-testid="stForm"] { padding: 1.35rem !important; border-radius: 16px !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _login_screen():
    _login_styles()
    st.markdown('<div class="login-shell">', unsafe_allow_html=True)
    with st.form("login_form", clear_on_submit=False):
        st.markdown(
            """
            <div class="login-kicker">Enterprise Sports Intelligence</div>
            <h1 class="login-title">SPORTA VISTA PRO</h1>
            <p class="login-subtitle">Secure role-based access for analysts, scouts, coaches, and administrators.</p>
            <div class="login-meta">
                <span class="login-pill">RBAC</span>
                <span class="login-pill">Live Analytics</span>
                <span class="login-pill">Secure Sessions</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        username = st.text_input("Username", placeholder="Enter your username")
        show_password = st.checkbox("Show password", value=False)
        password = st.text_input(
            "Password",
            type="default" if show_password else "password",
            placeholder="Enter your password"
        )
        st.write("")
        submit = st.form_submit_button("Sign In", use_container_width=True)

        if submit:
            clean_username = username.strip()
            if not clean_username or not password:
                st.error("Enter both username and password.")
            elif st.session_state.get("_auth_storage_unavailable"):
                st.error("Authentication storage is unavailable. Refresh the app and try again.")
            else:
                with st.spinner("Authenticating..."):
                    if login_user(clean_username, password, cookies):
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
    st.markdown('</div>', unsafe_allow_html=True)


login_page = st.Page(_login_screen, title="Login", icon=":material/lock:", default=True, url_path="login")

if is_authenticated():
    role = st.session_state.get("role")
    if not is_valid_role(role):
        logout_user(cookies)

    pages = _pages_for_role(role)
    if not pages:
        logout_user(cookies)

    pg = st.navigation(pages)
    show_sidebar_user_profile(cookies)
else:
    pg = st.navigation([login_page], position="hidden")

pg.run()
