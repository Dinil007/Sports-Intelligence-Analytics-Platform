"""
services/chat_transfer_service.py
===================================
Transfer intent detection and response service for AI Chat integration.

Allows the AI Chat assistant to recognise transfer-related requests and
delegate to the existing recommendation engine without going through the
SQL/LLM pipeline.

No Streamlit imports.
No UI rendering.
Returns only structured Python dictionaries.
"""

from __future__ import annotations

import re
from typing import Any

from services.recommendation_service import (
    recommend_similar_players,
)


# -------------------------------------------------------------------
# Keyword list — lightweight, no LLM
# -------------------------------------------------------------------
_TRANSFER_KEYWORDS = [
    "replace",
    "replacement",
    "similar player",
    "similar to",
    "recommend player",
    "recommend a",
    "recommend an",
    "budget striker",
    "budget forward",
    "young winger",
    "young forward",
    "transfer target",
    "alternative",
    "successor",
    "find a replacement",
    "find players similar",
    "suggest a replacement",
    "who can replace",
    "looking for a",
    "need a",
]


# -------------------------------------------------------------------
# Public helpers
# -------------------------------------------------------------------


def detect_transfer_intent(prompt: str) -> bool:
    """Return True when *prompt* contains transfer-related keywords.

    Lightweight keyword matching only — no LLM call.
    """
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in _TRANSFER_KEYWORDS)

def extract_target_player(prompt: str) -> str | None:
    """Extract the target player name from a transfer request.

    Examples
    --------
    ``"Suggest a replacement for Rodri"`` -> ``"Rodri"``
    ``"Find players similar to Kevin De Bruyne"`` -> ``"Kevin De Bruyne"``
    """
    # Patterns that introduce a player name
    patterns = [
        r"(?:replace|replacement for|similar to|similar as|like)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        r"(?:for)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
    ]
    for pat in patterns:
        m = re.search(pat, prompt)
        if m:
            return m.group(1).strip()

    # Fallback — last multi-word capitalized token group
    names = re.findall(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*", prompt)
    if names:
        return names[-1].strip()

    return None


def extract_optional_filters(prompt: str) -> dict[str, Any]:
    """Extract optional filters from a transfer request.

    Examples
    --------
    ``"young winger"``
        -> ``{"position": "Forward", "age_max": 23}``

    ``"budget striker"``
        -> ``{"position": "Forward", "budget_tier": "Low"}``

    Returns
    -------
    dict
        Empty when no filters can be derived.
    """
    filters: dict[str, Any] = {}
    prompt_lower = prompt.lower()

    # -- Position -----------------------------------------------------------
    position_map = {
        "striker": "Forward",
        "forward": "Forward",
        "winger": "Forward",
        "attacker": "Forward",
        "midfielder": "Midfielder",
        "midfield": "Midfielder",
        "defender": "Defender",
        "defensive": "Defender",
        "centre-back": "Defender",
        "center-back": "Defender",
        "full-back": "Defender",
        "fullback": "Defender",
        "goalkeeper": "Goalkeeper",
        "keeper": "Goalkeeper",
    }
    for keyword, position in position_map.items():
        if keyword in prompt_lower:
            filters["position"] = position
            break

    # -- Age ----------------------------------------------------------------
    age_patterns: list[tuple[str, str]] = [
        (r"young(?:er)?\s*(?:than\s*)?(\d+)", "age_max"),
        (r"under\s*(\d+)", "age_max"),
        (r"u(\d{2})\b", "age_max"),
        (r"age\s*(?:under|<)\s*(\d+)", "age_max"),
        (r"over\s*(\d+)", "age_min"),
        (r"age\s*(?:over|>)\s*(\d+)", "age_min"),
    ]
    for pat, field in age_patterns:
        m = re.search(pat, prompt_lower)
        if m:
            try:
                age = int(m.group(1))
                filters[field] = age
            except ValueError:
                pass

    if "young" in prompt_lower and "age_max" not in filters:
        filters["age_max"] = 23

    # -- Budget tier --------------------------------------------------------
    budget_map = {
        "budget": "Low",
        "cheap": "Low",
        "low-cost": "Low",
        "affordable": "Medium",
        "moderate": "Medium",
        "expensive": "High",
        "top": "Elite",
        "world-class": "Elite",
        "elite": "Elite",
    }
    for keyword, tier in budget_map.items():
        if keyword in prompt_lower:
            filters["budget_tier"] = tier
            break

    # -- Preferred foot -----------------------------------------------------
    if "left-foot" in prompt_lower or "left foot" in prompt_lower:
        filters["preferred_foot"] = "Left"
    elif "right-foot" in prompt_lower or "right foot" in prompt_lower:
        filters["preferred_foot"] = "Right"

    return filters


# -------------------------------------------------------------------
# Main entry point
# -------------------------------------------------------------------


def generate_transfer_response(prompt: str) -> dict[str, Any]:
    """Process *prompt* and return a structured transfer response.

    Flow
    ----
    1. ``detect_transfer_intent()``
    2. ``extract_target_player()``
    3. ``extract_optional_filters()``
    4. ``recommend_similar_players()``
    5. Return structured dict.

    Parameters
    ----------
    prompt : str
        The raw user question from AI Chat.

    Returns
    -------
    dict
        ``{"handled": True, "selected_player": ..., "recommendations": [...], "filters": {...}}``
        when the request is transfer-related.

        ``{"handled": False}``
        when the request is **not** transfer-related — the AI Chat should
        fall through to its normal LLM pipeline.
    """
    if not detect_transfer_intent(prompt):
        return {"handled": False}

    target_player = extract_target_player(prompt)
    filters = extract_optional_filters(prompt)

    # --- Call the existing recommendation engine ----------------------------
    if target_player:
        # Map our internal filter names to the service parameter names
        param_mapping = {
            "position": "position",
            "age_max": "age_max",
            "age_min": "age_min",
            "budget_tier": "budget_tier",
            "preferred_foot": "preferred_foot",
        }
        kwargs: dict[str, Any] = {"player_name": target_player}
        for our_key, service_key in param_mapping.items():
            if our_key in filters:
                kwargs[service_key] = filters[our_key]

        try:
            recommendations = recommend_similar_players(**kwargs)
        except Exception:
            recommendations = []

        return {
            "handled": True,
            "selected_player": target_player,
            "recommendations": recommendations,
            "filters": filters,
        }

    # Transfer intent detected but no player could be extracted
    return {
        "handled": True,
        "selected_player": None,
        "recommendations": [],
        "filters": filters,
        "error": "Could not identify a target player in your request.",
    }
