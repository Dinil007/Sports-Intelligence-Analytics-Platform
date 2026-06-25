"""Role and route authorization helpers for SPORTA VISTA PRO."""

VALID_ROLES = frozenset({"admin", "coach", "scout", "analyst"})


def normalize_role(role: str | None) -> str | None:
    if role is None:
        return None
    cleaned = str(role).strip().lower()
    return cleaned if cleaned in VALID_ROLES else None


def is_valid_role(role: str | None) -> bool:
    return normalize_role(role) in VALID_ROLES


def role_label(role: str | None) -> str:
    normalized = normalize_role(role)
    return normalized.title() if normalized else "Unknown"


def is_page_allowed(role: str | None, page_key: str, role_page_keys: dict[str, list[str]]) -> bool:
    normalized = normalize_role(role)
    if not normalized:
        return False
    return page_key in role_page_keys.get(normalized, [])
