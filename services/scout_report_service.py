"""
services/scout_report_service.py
===============================
AI-powered scouting report generation for player recommendations.

Reuses the project's existing Groq integration.
No Streamlit widgets are used here.
No SQL is executed here.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from groq import Groq

# ---------------------------------------------------------------------------
# Environment & Client
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

_MODEL = "llama-3.3-70b-versatile"

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """You are a professional football scout working for an elite European club.

Analyze the following player.

Generate a concise scouting report.

Return JSON only.

Do not include markdown.

Do not invent statistics.

Base your reasoning only on the supplied metrics."""

_FALLBACK: dict[str, Any] = {
    "strengths": [],
    "weaknesses": [],
    "playing_style": "Unavailable",
    "tactical_suitability": "Unavailable",
    "development_potential": "Unavailable",
    "transfer_risk": "Unavailable",
    "overall_verdict": "AI Scout Report unavailable.",
}

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_CACHE: dict[tuple[str, Any], dict[str, Any]] = {}


def _safe_str(value: Any, default: str = "Unknown") -> str:
    if value is None:
        return default
    s = str(value).strip()
    return s if s else default


def _build_prompt(player: dict[str, Any]) -> str:
    return f"""Analyze the following player:

Player Name: {_safe_str(player.get("player_name"))}
Club: {_safe_str(player.get("club"))}
Nationality: {_safe_str(player.get("nationality"))}
SPORTA Score: {_safe_str(player.get("sporta_score"))}
Similarity %: {_safe_str(player.get("similarity_pct"))}
Goals: {_safe_str(player.get("goals"))}
Assists: {_safe_str(player.get("assists"))}
xG: {_safe_str(player.get("total_xg"))}
Pass Accuracy: {_safe_str(player.get("pass_accuracy"))}
Passes: {_safe_str(player.get("passes"))}
Dribbles: {_safe_str(player.get("dribbles"))}
Carries: {_safe_str(player.get("carries"))}
Recoveries: {_safe_str(player.get("recoveries"))}
Pressures: {_safe_str(player.get("pressures"))}
Minutes Played: {_safe_str(player.get("minutes_played"))}
Age: {_safe_str(player.get("age"))}
Position: {_safe_str(player.get("position"))}
Preferred Foot: {_safe_str(player.get("preferred_foot"))}"""


def _parse_ai_response(raw: str) -> dict[str, Any]:
    """Parse the AI response into structured scout report data."""
    text = raw.strip()

    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [line for line in lines if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()

    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return dict(_FALLBACK)

    result = dict(_FALLBACK)
    result["strengths"] = data.get("strengths", [])
    result["weaknesses"] = data.get("weaknesses", [])
    result["playing_style"] = data.get("playing_style", "Unavailable") or "Unavailable"
    result["tactical_suitability"] = (
        data.get("tactical_suitability", "Unavailable") or "Unavailable"
    )
    result["development_potential"] = (
        data.get("development_potential", "Unavailable") or "Unavailable"
    )
    result["transfer_risk"] = data.get("transfer_risk", "Unavailable") or "Unavailable"
    result["overall_verdict"] = (
        data.get("overall_verdict", _FALLBACK["overall_verdict"])
        or _FALLBACK["overall_verdict"]
    )

    # Ensure strengths/weaknesses are lists
    if not isinstance(result["strengths"], list):
        result["strengths"] = [str(result["strengths"])] if result["strengths"] else []
    if not isinstance(result["weaknesses"], list):
        result["weaknesses"] = [str(result["weaknesses"])] if result["weaknesses"] else []

    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_scout_report(player: dict[str, Any]) -> dict[str, Any]:
    """
    Generate an AI scouting report for a player.

    Parameters
    ----------
    player : dict[str, Any]
        Player data containing metrics such as player_name, club, sporta_score,
        similarity_pct, goals, assists, pass_accuracy, etc.

    Returns
    -------
    dict[str, Any]
        Structured report with keys:
        - strengths: list[str]
        - weaknesses: list[str]
        - playing_style: str
        - tactical_suitability: str
        - development_potential: str
        - transfer_risk: str
        - overall_verdict: str
    """
    if not player:
        return dict(_FALLBACK)

    cache_key = (
        _safe_str(player.get("player_name")),
        player.get("similarity_pct"),
    )
    if cache_key in _CACHE:
        return _CACHE[cache_key]

    prompt = _build_prompt(player)

    try:
        response = _client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1024,
        )
        raw_content = response.choices[0].message.content
        if not raw_content:
            result = dict(_FALLBACK)
        else:
            result = _parse_ai_response(raw_content)
    except Exception:
        result = dict(_FALLBACK)

    _CACHE[cache_key] = result
    return dict(result)