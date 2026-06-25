import sys
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

_auth_dir = str(Path(__file__).resolve().parent)
while _auth_dir in sys.path:
    sys.path.remove(_auth_dir)

from jose import jwt

from auth.auth_guard import VALID_ROLES, is_page_allowed, is_valid_role, normalize_role
from auth.auth_service import AuthenticatedUser
from auth.navigation import PAGE_DEFINITIONS, ROLE_PAGE_KEYS, get_page_paths_for_role
from auth.security import (
    ALGORITHM,
    AUTH_COOKIE_KEY,
    SECRET_KEY,
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)


class FakeSessionState(dict):
    def __init__(self, *args, protected_keys=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.protected_keys = set(protected_keys or ())
        self.deleted_keys = []
        self.assigned_keys = []

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as exc:
            raise AttributeError(key) from exc

    def __setattr__(self, key, value):
        if key in {"protected_keys", "deleted_keys", "assigned_keys"}:
            object.__setattr__(self, key, value)
            return
        if key in self.protected_keys and key in self:
            raise RuntimeError(f"Cannot modify protected key {key}")
        self.assigned_keys.append(key)
        self[key] = value

    def __setitem__(self, key, value):
        if hasattr(self, "protected_keys") and key in self.protected_keys and key in self:
            raise RuntimeError(f"Cannot modify protected key {key}")
        super().__setitem__(key, value)

    def __delitem__(self, key):
        self.deleted_keys.append(key)
        super().__delitem__(key)


def fake_st(session_state=None):
    return SimpleNamespace(
        session_state=session_state or FakeSessionState(),
        cache_data=SimpleNamespace(clear=MagicMock()),
        cache_resource=SimpleNamespace(clear=MagicMock()),
        rerun=MagicMock(),
        sidebar=MagicMock(),
        markdown=MagicMock(),
    )


def test_password_hashing():
    password = "supersecretpassword123"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_token_creation_and_decoding():
    data = {"sub": "test_user", "role": "coach", "email": "coach@test.com"}
    token = create_access_token(data)
    payload = decode_access_token(token)
    assert payload is not None
    assert payload.get("sub") == "test_user"
    assert payload.get("role") == "coach"


def test_expired_token_is_rejected():
    expired_payload = {
        "sub": "test_user",
        "role": "coach",
        "exp": datetime.utcnow() - timedelta(minutes=1),
    }
    token = jwt.encode(expired_payload, SECRET_KEY, algorithm=ALGORITHM)
    assert decode_access_token(token) is None


def test_invalid_token_is_rejected():
    assert decode_access_token("not-a-valid-token") is None
    assert decode_access_token("") is None
    assert decode_access_token(None) is None


def test_session_token_contains_fresh_session_identity():
    from auth.token_manager import create_session_token, decode_session_token

    token = create_session_token(
        user_id=10,
        username="admin",
        email="admin@test.com",
        role="admin",
        session_id="session-123",
    )
    payload = decode_session_token(token)
    assert payload["sub"] == "admin"
    assert payload["user_id"] == 10
    assert payload["role"] == "admin"
    assert payload["session_id"] == "session-123"


def test_get_stored_token_ignores_empty_cookie():
    from auth.token_manager import get_stored_token

    cookies = MagicMock()
    for empty in ("", "   ", "{}", "null", '""'):
        cookies.get.return_value = empty
        assert get_stored_token(cookies) is None

    cookies.get.return_value = "valid-token"
    assert get_stored_token(cookies) == "valid-token"


def test_clear_auth_cookie_removes_value():
    from auth.token_manager import clear_auth_cookie

    cookies = MagicMock()
    clear_auth_cookie(cookies)
    cookies.__setitem__.assert_called_with(AUTH_COOKIE_KEY, "")
    cookies.save.assert_called_once()


def test_role_normalization_and_rbac():
    assert normalize_role("Admin") == "admin"
    assert normalize_role(" scout ") == "scout"
    assert normalize_role("owner") is None
    assert is_valid_role("coach")
    assert not is_valid_role("superadmin")
    assert is_page_allowed("admin", "admin_panel", ROLE_PAGE_KEYS)
    assert not is_page_allowed("scout", "admin_panel", ROLE_PAGE_KEYS)


def test_validate_token_rejects_role_spoofing():
    from auth.auth_service import validate_token
    from auth.token_manager import create_session_token

    database_user = AuthenticatedUser(user_id=1, username="admin", email="admin@test.com", role="admin")
    spoofed_token = create_session_token(
        user_id=1,
        username="admin",
        email="admin@test.com",
        role="scout",
        session_id="spoofed",
    )

    with patch("auth.auth_service.get_user_by_username", return_value=database_user):
        assert validate_token(spoofed_token) is None


def test_validate_token_restores_database_user_role():
    from auth.auth_service import validate_token
    from auth.token_manager import create_session_token

    database_user = AuthenticatedUser(user_id=2, username="scout", email="scout@test.com", role="scout")
    token = create_session_token(
        user_id=2,
        username="scout",
        email="scout@test.com",
        role="scout",
        session_id="fresh-session",
    )

    with patch("auth.auth_service.get_user_by_username", return_value=database_user):
        resolved = validate_token(token)

    assert resolved is not None
    user, payload = resolved
    assert user.role == "scout"
    assert payload["session_id"] == "fresh-session"


def test_start_authenticated_session_clears_previous_user():
    from auth.session_manager import start_authenticated_session

    queue = {"existing": {"value": "cookie", "path": "/"}}
    state = FakeSessionState({
        "authenticated": True,
        "user_id": 99,
        "username": "old_admin",
        "email": "old@test.com",
        "role": "admin",
        "custom_old_key": "must disappear",
        "CookieManager.queue": queue,
    })
    st_obj = fake_st(state)
    scout = AuthenticatedUser(user_id=3, username="scout", email="scout@test.com", role="scout")

    with patch("auth.session_manager.st", st_obj):
        start_authenticated_session(scout, "token-abc", "session-abc")

    assert state["authenticated"] is True
    assert state["user_id"] == 3
    assert state["username"] == "scout"
    assert state["email"] == "scout@test.com"
    assert state["role"] == "scout"
    assert state["session_id"] == "session-abc"
    assert state["auth_token"] == "token-abc"
    assert state["CookieManager.queue"] is queue
    assert "custom_old_key" not in state


def test_ensure_authenticated_clears_invalid_token_and_session():
    from auth.streamlit_auth import ensure_authenticated

    state = FakeSessionState({"authenticated": True, "username": "ghost", "role": "admin"})
    st_obj = fake_st(state)
    cookies = MagicMock()
    cookies.get.return_value = "bad-token"

    with patch("auth.streamlit_auth.st", st_obj), patch("auth.session_manager.st", st_obj):
        assert ensure_authenticated(cookies) is False

    cookies.__setitem__.assert_called_with(AUTH_COOKIE_KEY, "")
    assert state["authenticated"] is False
    assert state["username"] is None
    assert state["role"] is None


def test_ensure_authenticated_restores_valid_token_user():
    from auth.streamlit_auth import ensure_authenticated

    state = FakeSessionState({"username": "previous", "role": "admin"})
    st_obj = fake_st(state)
    cookies = MagicMock()
    cookies.get.return_value = "valid-token"
    user = AuthenticatedUser(user_id=4, username="coach", email="coach@test.com", role="coach")

    with patch("auth.streamlit_auth.st", st_obj), patch("auth.session_manager.st", st_obj):
        with patch("auth.streamlit_auth.validate_token", return_value=(user, {"session_id": "coach-session"})):
            assert ensure_authenticated(cookies) is True

    assert state["authenticated"] is True
    assert state["user_id"] == 4
    assert state["username"] == "coach"
    assert state["email"] == "coach@test.com"
    assert state["role"] == "coach"
    assert state["session_id"] == "coach-session"
    assert state["auth_token"] == "valid-token"


def test_login_user_generates_new_clean_session():
    from auth.streamlit_auth import login_user

    state = FakeSessionState({"username": "admin", "role": "admin", "stale": "remove"})
    st_obj = fake_st(state)
    cookies = MagicMock()
    user = AuthenticatedUser(user_id=5, username="analyst", email="analyst@test.com", role="analyst")

    with patch("auth.streamlit_auth.st", st_obj), patch("auth.session_manager.st", st_obj):
        with patch("auth.streamlit_auth.authenticate_credentials", return_value=user):
            assert login_user("analyst", "password", cookies) is True

    assert state["authenticated"] is True
    assert state["username"] == "analyst"
    assert state["role"] == "analyst"
    assert state["session_id"]
    assert state["auth_token"]
    assert "stale" not in state
    cookies.__setitem__.assert_called_once()
    cookies.save.assert_called_once()


def test_logout_user_clears_cookie_cache_session_and_reruns():
    from auth.streamlit_auth import logout_user

    state = FakeSessionState({"authenticated": True, "username": "admin", "role": "admin"})
    st_obj = fake_st(state)
    cookies = MagicMock()

    with patch("auth.streamlit_auth.st", st_obj), patch("auth.session_manager.st", st_obj):
        logout_user(cookies)

    cookies.__setitem__.assert_called_with(AUTH_COOKIE_KEY, "")
    assert cookies.save.call_count == 2
    st_obj.cache_data.clear.assert_called_once()
    st_obj.cache_resource.clear.assert_called_once()
    st_obj.rerun.assert_called_once()
    assert state["authenticated"] is False
    assert state["username"] is None
    assert state["role"] is None


def test_logout_preserves_cookie_delete_queue_only():
    from auth.streamlit_auth import logout_user

    delete_queue = {AUTH_COOKIE_KEY: {"value": None, "path": "/"}}
    state = FakeSessionState({
        "authenticated": True,
        "username": "admin",
        "role": "admin",
        "auth_token": "old-admin-token",
        "dashboard_filter": "must disappear",
        "CookieManager.queue": delete_queue,
    }, protected_keys={"CookieManager.queue"})
    st_obj = fake_st(state)
    cookies = MagicMock()

    with patch("auth.streamlit_auth.st", st_obj), patch("auth.session_manager.st", st_obj):
        logout_user(cookies)

    assert state["CookieManager.queue"] is delete_queue
    assert state["authenticated"] is False
    assert state["auth_token"] is None
    assert "dashboard_filter" not in state
    assert "CookieManager.queue" not in state.deleted_keys


def test_logout_retries_cookie_deletion_if_session_cleanup_fails():
    from auth.streamlit_auth import logout_user

    state = FakeSessionState({"authenticated": True, "username": "admin", "role": "admin"})
    st_obj = fake_st(state)
    cookies = MagicMock()

    with patch("auth.streamlit_auth.st", st_obj), patch("auth.session_manager.st", st_obj):
        with patch("auth.streamlit_auth.clear_auth_session", side_effect=RuntimeError("session cleanup failed")):
            logout_user(cookies)

    assert cookies.__setitem__.call_count == 2
    cookies.__setitem__.assert_any_call(AUTH_COOKIE_KEY, "")
    assert cookies.save.call_count == 2
    st_obj.rerun.assert_called_once()


def test_ensure_authenticated_keeps_current_session_route_state_when_token_matches():
    from auth.streamlit_auth import ensure_authenticated

    state = FakeSessionState({
        "authenticated": True,
        "user_id": 1,
        "username": "admin",
        "email": "admin@test.com",
        "role": "admin",
        "session_id": "same-session",
        "auth_token": "same-token",
        "_page_registry": {"current": "player_comparison"},
    })
    st_obj = fake_st(state)
    cookies = MagicMock()
    cookies.get.return_value = "same-token"

    with patch("auth.streamlit_auth.st", st_obj), patch("auth.session_manager.st", st_obj):
        with patch("auth.streamlit_auth.validate_token") as mock_validate:
            assert ensure_authenticated(cookies) is True

    mock_validate.assert_not_called()
    assert state["_page_registry"] == {"current": "player_comparison"}
    assert state["username"] == "admin"


def test_all_roles_have_navigation_pages():
    for role in VALID_ROLES:
        assert is_valid_role(role), f"Role {role} should be valid"
        paths = get_page_paths_for_role(role)
        assert paths, f"Role {role} must have at least one page"
        assert paths[0].endswith("Home.py"), f"Role {role} must start with Home"
        assert len(paths) == len(set(paths)), f"Role {role} has duplicate page paths"


def test_role_page_keys_reference_known_definitions():
    for role, keys in ROLE_PAGE_KEYS.items():
        for key in keys:
            assert key in PAGE_DEFINITIONS, f"Unknown page key {key!r} for role {role}"


if __name__ == "__main__":
    tests = [
        test_password_hashing,
        test_token_creation_and_decoding,
        test_expired_token_is_rejected,
        test_invalid_token_is_rejected,
        test_session_token_contains_fresh_session_identity,
        test_get_stored_token_ignores_empty_cookie,
        test_clear_auth_cookie_removes_value,
        test_role_normalization_and_rbac,
        test_validate_token_rejects_role_spoofing,
        test_validate_token_restores_database_user_role,
        test_start_authenticated_session_clears_previous_user,
        test_ensure_authenticated_clears_invalid_token_and_session,
        test_ensure_authenticated_restores_valid_token_user,
        test_login_user_generates_new_clean_session,
        test_logout_user_clears_cookie_cache_session_and_reruns,
        test_logout_preserves_cookie_delete_queue_only,
        test_logout_retries_cookie_deletion_if_session_cleanup_fails,
        test_ensure_authenticated_keeps_current_session_route_state_when_token_matches,
        test_all_roles_have_navigation_pages,
        test_role_page_keys_reference_known_definitions,
    ]

    print("=== Running Authentication Tests ===")
    failed = 0
    for test in tests:
        print(f"[TEST] {test.__name__}...")
        try:
            test()
            print(f"[SUCCESS] {test.__name__}")
        except Exception as exc:
            failed += 1
            print(f"[FAILED] {test.__name__}: {exc}")

    if failed:
        print(f"\n[ERROR] {failed} test(s) failed.")
        sys.exit(1)
    print("\n[SUCCESS] All authentication checks passed successfully!")
