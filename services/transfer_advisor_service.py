"""
services/transfer_advisor_service.py
=====================================
AI-powered transfer advisor that produces an executive recommendation.

Reuses the project's existing Groq integration from scout_report_service.py.
No Streamlit widgets. No SQL.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from groq import Groq

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
_MODEL = "llama-3.3-70b-versatile"
_CACHE: dict[tuple[Any, ...], dict[str, Any]] = {}


def _fallback_advisor() -> dict[str, Any]:
    return {
        "best_replacement": "Unavailable",
        "recommendation_score": 0.0,
        "confidence": 0.0,
        "estimated_transfer_fee": "Unavailable",
        "transfer_risk": "Unavailable",
        "development_potential": "Unavailable",
        "contract_suitability": "Unavailable",
        "tactical_fit": "Unavailable",
        "top_reasons": [],
        "alternative_targets": [],
        "recruitment_priority": "★☆☆☆☆",
        "final_verdict": "AI Transfer Advisor unavailable.",
    }


def _safe_str(value: Any, default: str = "Unknown") -> str:
    if value is None:
        return default
    s = str(value).strip()
    return s if s else default


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        f = float(value)
        return f if f == f else default
    except (TypeError, ValueError):
        return default


def _build_prompt(selected_player: dict[str, Any], recommendations: list[dict[str, Any]]) -> str:
    sp = selected_player or {}
    rec_lines = []
    for r in recommendations[:5]:
        rec_lines.append(
            f"- {_safe_str(r.get('player_name'))} | {_safe_str(r.get('club'))} | "
            f"SPORTA: {_safe_str(r.get('sporta_score'))} | RecScore: {_safe_str(r.get('recommendation_score'))} | "
            f"Similarity: {_safe_str(r.get('similarity_pct'))}% | Goals: {_safe_str(r.get('goals'))} | "
            f"Assists: {_safe_str(r.get('assists'))} | xG: {_safe_str(r.get('total_xg'))} | "
            f"Passes: {_safe_str(r.get('passes'))} | Dribbles: {_safe_str(r.get('dribbles'))} | "
            f"Carries: {_safe_str(r.get('carries'))} | Recoveries: {_safe_str(r.get('recoveries'))} | "
            f"Pressures: {_safe_str(r.get('pressures'))} | Minutes: {_safe_str(r.get('minutes_played'))} | "
            f"Foot: {_safe_str(r.get('preferred_foot'))}"
        )

    prompt = f"""You are an elite football transfer advisor.

Selected player to replace:
Name: {_safe_str(sp.get('player_name'))}
Club: {_safe_str(sp.get('club'))}
Nationality: {_safe_str(sp.get('nationality'))}
Position: {_safe_str(sp.get('position'))}
Age: {_safe_str(sp.get('age'))}
SPORTA Score: {_safe_str(sp.get('sporta_score'))}
Similarity %: {_safe_str(sp.get('similarity_pct'))}

Top recommendations:
{chr(10).join(rec_lines) if rec_lines else 'None available'}

Task:
1. Pick exactly ONE best replacement from the recommendations above.
2. Score it 0-100 on recommendation_score and confidence (each float).
3. Estimate a realistic transfer fee tier only (e.g. "€25M-35M", "Free transfer").
4. Assess transfer risk, development potential, contract suitability, tactical fit.
5. Provide 5 concise top_reasons.
6. Provide 3 alternative_targets (must be from the recommendation list).
7. Rate recruitment priority as stars 1-5 in format "★☆☆☆☆" to "★★★★★".
8. Write a 2-3 sentence final verdict.

Return JSON ONLY with these exact keys:
{{
    "best_replacement": str,
    "recommendation_score": float,
    "confidence": float,
    "estimated_transfer_fee": str,
    "transfer_risk": str,
    "development_potential": str,
    "contract_suitability": str,
    "tactical_fit": str,
    "top_reasons": [str, str, str, str, str],
    "alternative_targets": [str, str, str],
    "recruitment_priority": "★☆☆☆☆" to "★★★★★",
    "final_verdict": str
}}

Do not invent statistics. Base reasoning only on supplied metrics."""
    return prompt


def _parse_ai_response(raw: str) -> dict[str, Any]:
    """Parse the AI response into the transfer advisor schema."""
    text = raw.strip()

    if text.startswith("```"):
        lines = text.split("\n")
        lines = [line for line in lines if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()

    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return dict(_fallback_advisor())

    result = dict(_fallback_advisor())
    result["best_replacement"] = _safe_str(data.get("best_replacement"), "Unavailable")
    result["recommendation_score"] = _safe_float(data.get("recommendation_score"), 0.0)
    result["confidence"] = _safe_float(data.get("confidence"), 0.0)
    result["estimated_transfer_fee"] = _safe_str(data.get("estimated_transfer_fee"), "Unavailable")
    result["transfer_risk"] = _safe_str(data.get("transfer_risk"), "Unavailable")
    result["development_potential"] = _safe_str(data.get("development_potential"), "Unavailable")
    result["contract_suitability"] = _safe_str(data.get("contract_suitability"), "Unavailable")
    result["tactical_fit"] = _safe_str(data.get("tactical_fit"), "Unavailable")

    reasons = data.get("top_reasons", [])
    if not isinstance(reasons, list):
        reasons = [str(reasons)] if reasons else []
    result["top_reasons"] = [str(r) for r in reasons[:5]]
    while len(result["top_reasons"]) < 5:
        result["top_reasons"].append("")

    alt = data.get("alternative_targets", [])
    if not isinstance(alt, list):
        alt = [str(alt)] if alt else []
    result["alternative_targets"] = [str(a) for a in alt[:3]]
    while len(result["alternative_targets"]) < 3:
        result["alternative_targets"].append("")

    priority = _safe_str(data.get("recruitment_priority"), "★☆☆☆☆")
    valid_priorities = {"★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★"}
    if priority not in valid_priorities:
        priority = "★☆☆☆☆"
    result["recruitment_priority"] = priority

    result["final_verdict"] = _safe_str(data.get("final_verdict"), "AI Transfer Advisor unavailable.")

    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_transfer_advisor(
    selected_player: dict[str, Any],
    recommendations: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Generate an AI transfer advisor recommendation.

    Parameters
    ----------
    selected_player : dict[str, Any]
        The reference player being replaced.
    recommendations : list[dict[str, Any]]
        Generated recommendation list from recommend_similar_players().

    Returns
    -------
    dict[str, Any]
        Structured transfer advisor response matching the required schema.
        Never raises; returns fallback on any failure.
    """
    if not selected_player or not recommendations:
        return dict(_fallback_advisor())

    cache_key = (
        _safe_str(selected_player.get("player_name")),
        tuple(_safe_str(r.get("player_name")) for r in recommendations),
    )
    if cache_key in _CACHE:
        return dict(_CACHE[cache_key])

    prompt = _build_prompt(selected_player, recommendations)

    try:
        response = _client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional football transfer advisor. Return JSON only. Do not include markdown."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1024,
        )
        raw_content = response.choices[0].message.content
        if not raw_content:
            result = dict(_fallback_advisor())
        else:
            result = _parse_ai_response(raw_content)
    except Exception:
        result = dict(_fallback_advisor())

    _CACHE[cache_key] = result
    return dict(result)


