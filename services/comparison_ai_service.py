"""
services/comparison_ai_service.py
===================================
AI-powered comparison verdict between two players.

Reuses the project's existing Groq integration pattern.
No Streamlit. No SQL. No repository imports.
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


def _fallback_verdict() -> dict[str, Any]:
    return {
        "winner": "N/A",
        "confidence": 0.0,
        "strengths": [],
        "weaknesses": [],
        "risk": "Unavailable",
        "verdict": "AI Comparison Verdict unavailable.",
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


def _build_prompt(selected: dict[str, Any], recommended: dict[str, Any]) -> str:
    sel = selected or {}
    rec = recommended or {}
    return f"""You are an elite football analyst comparing two players.

Player A (Selected):
Name: {_safe_str(sel.get('player_name'))}
Club: {_safe_str(sel.get('club'))}
Position: {_safe_str(sel.get('position'))}
SPORTA Score: {_safe_str(sel.get('sporta_score'))}
Similarity: {_safe_str(sel.get('similarity_pct'))}
Goals: {_safe_str(sel.get('goals'))}
Assists: {_safe_str(sel.get('assists'))}
xG: {_safe_str(sel.get('total_xg'))}
Pass Accuracy: {_safe_str(sel.get('pass_accuracy'))}
Passes: {_safe_str(sel.get('passes'))}
Dribbles: {_safe_str(sel.get('dribbles'))}
Carries: {_safe_str(sel.get('carries'))}
Recoveries: {_safe_str(sel.get('recoveries'))}
Pressures: {_safe_str(sel.get('pressures'))}

Player B (Recommended):
Name: {_safe_str(rec.get('player_name'))}
Club: {_safe_str(rec.get('club'))}
Position: {_safe_str(rec.get('position'))}
SPORTA Score: {_safe_str(rec.get('sporta_score'))}
Similarity: {_safe_str(rec.get('similarity_pct'))}
Goals: {_safe_str(rec.get('goals'))}
Assists: {_safe_str(rec.get('assists'))}
xG: {_safe_str(rec.get('total_xg'))}
Pass Accuracy: {_safe_str(rec.get('pass_accuracy'))}
Passes: {_safe_str(rec.get('passes'))}
Dribbles: {_safe_str(rec.get('dribbles'))}
Carries: {_safe_str(rec.get('carries'))}
Recoveries: {_safe_str(rec.get('recoveries'))}
Pressures: {_safe_str(rec.get('pressures'))}

Compare Player A vs Player B. Return JSON ONLY:
{{"winner": "Player A"|"Player B"|"Even", "confidence": float, "strengths": [str]*5, "weaknesses": [str]*3, "risk": str, "verdict": str}}
Do not invent statistics."""


def _parse_response(raw: str) -> dict[str, Any]:
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [line for line in lines if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return dict(_fallback_verdict())
    result = dict(_fallback_verdict())
    result["winner"] = _safe_str(data.get("winner"), "N/A")
    result["confidence"] = _safe_float(data.get("confidence"), 0.0)
    result["risk"] = _safe_str(data.get("risk"), "Unavailable")
    result["verdict"] = _safe_str(data.get("verdict"), "AI Comparison Verdict unavailable.")
    strengths = data.get("strengths", [])
    if not isinstance(strengths, list):
        strengths = [str(strengths)] if strengths else []
    result["strengths"] = [str(s) for s in strengths[:5]]
    while len(result["strengths"]) < 5:
        result["strengths"].append("")
    weaknesses = data.get("weaknesses", [])
    if not isinstance(weaknesses, list):
        weaknesses = [str(weaknesses)] if weaknesses else []
    result["weaknesses"] = [str(w) for w in weaknesses[:3]]
    while len(result["weaknesses"]) < 3:
        result["weaknesses"].append("")
    return result


def generate_comparison_verdict(
    selected_player: dict[str, Any],
    recommended_player: dict[str, Any],
) -> dict[str, Any]:
    if not selected_player or not recommended_player:
        return dict(_fallback_verdict())
    cache_key = (
        _safe_str(selected_player.get("player_name")),
        _safe_str(recommended_player.get("player_name")),
    )
    if cache_key in _CACHE:
        return dict(_CACHE[cache_key])
    prompt = _build_prompt(selected_player, recommended_player)
    try:
        response = _client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional football analyst. Return JSON only. Do not include markdown."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1024,
        )
        raw_content = response.choices[0].message.content
        result = _parse_response(raw_content) if raw_content else dict(_fallback_verdict())
    except Exception:
        result = dict(_fallback_verdict())
    _CACHE[cache_key] = result
    return dict(result)


