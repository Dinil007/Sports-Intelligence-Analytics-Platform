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
_CACHE: dict[str, dict[str, Any]] = {}


def _safe_str(value: Any, default: str = "Unknown") -> str:
    if value is None:
        return default
    s = str(value).strip()
    return s if s else default


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        f = float(value)
        return f if f == f else default
    except (TypeError, ValueError):
        return default


def _extract_kpis(match_dashboard: dict[str, Any]) -> dict[str, Any]:
    """Extract KPIs from match_dashboard."""
    events = match_dashboard.get("events", [])
    team_stats = match_dashboard.get("team_statistics", {})
    metrics = team_stats.get("metrics", {})
    home_team = _safe_str(match_dashboard.get("home_team"))
    away_team = _safe_str(match_dashboard.get("away_team"))

    event_counts: dict[str, int] = {}
    for e in events:
        etype = _safe_str(e.get("event_type"))
        event_counts[etype] = event_counts.get(etype, 0) + 1

    home_metrics = metrics.get(home_team, {}) if home_team else {}
    away_metrics = metrics.get(away_team, {}) if away_team else {}

    return {
        "home_team": home_team,
        "away_team": away_team,
        "total_events": len(events),
        "passes": event_counts.get("Pass", 0),
        "shots": event_counts.get("Shot", 0),
        "carries": event_counts.get("Carry", 0),
        "pressures": event_counts.get("Pressure", 0),
        "tackles": event_counts.get("Tackle", 0),
        "interceptions": event_counts.get("Interception", 0),
        "blocks": event_counts.get("Block", 0),
        "clearances": event_counts.get("Clearance", 0),
        "recoveries": event_counts.get("Ball Recovery", 0),
    }


def _generate_fallback_analysis(match_dashboard: dict[str, Any]) -> dict[str, Any]:
    """Generate realistic tactical analysis without AI."""
    kpis = _extract_kpis(match_dashboard)
    home = kpis["home_team"]
    away = kpis["away_team"]

    total_events = kpis["total_events"]
    passes = kpis["passes"]
    shots = kpis["shots"]
    tackles = kpis["tackles"]
    pressures = kpis["pressures"]
    recoveries = kpis["recoveries"]

    summary = (
        f"{home} and {away} contested a match with {total_events} total events. "
        f"{home} completed {passes} passes and took {shots} shots, "
        f"while {away} recorded {tackles} tackles and {pressures} pressures. "
        f"Both sides showed periods of control but lacked the final-ball quality to dominate."
    )

    strengths = {
        home: [
            "Composed build-up play from the back",
            "Effective use of wide channels to create overloads",
            "Solid mid-block structure limiting space between the lines",
        ],
        away: [
            "Disciplined defensive shape and coordinated pressing triggers",
            "Quick transitions exploiting half-spaces",
            "Strong ball-recovery intensity in the opposition half",
        ],
    }

    weaknesses = {
        home: [
            "Lack of penetration in the final third despite possession",
            "Slow transition tempo when turnovers occur",
            "Set-piece delivery and aerial duels need improvement",
        ],
        away: [
            "Shot selection and xG conversion below expectation",
            "Vulnerable to counter-pressing after losing possession",
            "Defensive spacing inclines when defending crosses",
        ],
    }

    recommendations = {
        "Attack": [
            "Increase progressive passes into the penalty area",
            "Improve shot quality from central positions",
            "Use wider wingers to stretch the defensive block",
        ],
        "Midfield": [
            "Rotate midfield units to maintain overloads during buildup",
            "Increase tempo in transition after ball recovery",
            "Improve defensive spacing when out of possession",
        ],
        "Defence": [
            "Improve communication on defensive set pieces",
            "Increase pressing triggers to force turnovers higher up the pitch",
            "Reduce counter-pressing vulnerability with quicker recovery runs",
        ],
    }

    verdict = {
        "winner": "Draw or low-scoring win",
        "score": "N/A",
        "reasoning": (
            "Both sides demonstrated structured tactical approaches but lacked decisive quality in the final third. "
            "Small margins in shot efficiency and transition speed could determine the outcome."
        ),
    }

    return {
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "verdict": verdict,
    }


def _build_tactical_prompt(match_dashboard: dict[str, Any]) -> str:
    """Build prompt for AI tactical analysis."""
    kpis = _extract_kpis(match_dashboard)
    home = kpis["home_team"]
    away = kpis["away_team"]

    return f"""You are an elite football tactical analyst. Analyze this match STRICTLY using football terminology.

Match: {home} vs {away}

Key Statistics:
- Total Events: {kpis['total_events']}
- Passes: {kpis['passes']} total
- Shots: {kpis['shots']} total
- Carries: {kpis['carries']} total
- Pressures: {kpis['pressures']} total
- Tackles: {kpis['tackles']} total
- Recoveries: {kpis['recoveries']} total

Return STRICT JSON only. Do not include markdown.

JSON schema:
{{
  "summary": "A 3-5 sentence executive summary using football language.",
  "strengths": {{
    "<Home Team>": ["...", "...", "..."],
    "<Away Team>": ["...", "...", "..."]
  }},
  "weaknesses": {{
    "<Home Team>": ["...", "...", "..."],
    "<Away Team>": ["...", "...", "..."]
  }},
  "recommendations": {{
    "<Home Team>": ["...", "...", "..."],
    "<Away Team>": ["...", "...", "..."]
  }},
  "verdict": {{
    "winner": "",
    "score": "",
    "reasoning": ""
  }}
}}

Requirements:
- summary: 3-5 sentences, executive tactical summary.
- strengths: each team must have 3-5 tactical strengths ONLY. Football terms: high pressing, wing overloads, midfield dominance, effective counter attacks, compact defensive block, progressive passing, possession control, ball recovery, final-third entries, transition play, set-piece threat, defensive organisation.
- weaknesses: each team must have 3-5 tactical weaknesses ONLY. Football terms: poor finishing, low xG creation, weak aerial duels, slow transitions, poor pressing, defensive gaps, loss of possession, counter attack vulnerability.
- recommendations: each team must have 3-5 coaching recommendations ONLY. Football terms: increase width, press higher, improve defensive spacing, create overloads, exploit half spaces, improve shot quality, rotate midfield, increase tempo.
- verdict: ONLY use keys: winner, score, reasoning. Do NOT use match_result, analysis, performance_rating, key_takeaway, mvp, or any other key."""


def _parse_tactical_response(raw: str) -> dict[str, Any]:
    """Parse AI response, preserving structured Python types."""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [line for line in lines if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return {}

    summary = data.get("summary", "")
    if isinstance(summary, str):
        pass
    elif isinstance(summary, dict):
        parts: list[str] = []
        match_val = summary.get("match")
        if match_val:
            parts.append(f"Match: {match_val}")
        desc = summary.get("description")
        if desc:
            parts.append(str(desc))
        ks = summary.get("key_statistics")
        if isinstance(ks, dict):
            parts.append("Key Statistics")
            for key in ("Total Events", "Passes", "Shots", "Carries", "Pressures", "Tackles", "Recoveries"):
                val = ks.get(key.lower().replace(" ", "_"))
                if val is None:
                    val = ks.get(key)
                if val is not None:
                    parts.append(f"• {key}: {val}")
        summary = "\n\n".join(parts) if parts else ""
    else:
        summary = ""

    def _make_dict(v: Any) -> dict:
        if isinstance(v, dict):
            return {str(k): [str(i) for i in (vv if isinstance(vv, list) else [vv]) if i is not None] for k, vv in v.items()}
        if isinstance(v, list):
            return {"Both Teams": [str(item) for item in v if item is not None]}
        return {}

    verdict = data.get("verdict", {})
    if isinstance(verdict, str):
        try:
            parsed = json.loads(verdict)
            if isinstance(parsed, dict):
                verdict = parsed
        except (json.JSONDecodeError, TypeError):
            verdict = {}
    if not isinstance(verdict, dict):
        verdict = {"winner": "N/A", "score": "N/A", "reasoning": str(verdict)}

    normalized_verdict = {
        "winner": str(
            verdict.get("winner") or
            verdict.get("result") or
            verdict.get("match_result") or
            "N/A"
        ),
        "score": str(
            verdict.get("score") or
            "N/A"
        ),
        "reasoning": str(
            verdict.get("reasoning") or
            verdict.get("description") or
            verdict.get("key_takeaway") or
            verdict.get("analysis") or
            verdict.get("tactical_implications") or
            ""
        ),
    }

    return {
        "summary": summary,
        "strengths": _make_dict(data.get("strengths")),
        "weaknesses": _make_dict(data.get("weaknesses")),
        "recommendations": _make_dict(data.get("recommendations")),
        "verdict": normalized_verdict,
    }


def _call_ai_tactical_analysis(match_dashboard: dict[str, Any]) -> dict[str, Any]:
    """Call Groq API for tactical analysis."""
    prompt = _build_tactical_prompt(match_dashboard)
    try:
        response = _client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional football analyst. Return STRICT JSON only. Do not use markdown code blocks."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1024,
        )
        raw_content = response.choices[0].message.content
        if raw_content:
            result = _parse_tactical_response(raw_content)
            if result:
                return result
    except Exception:
        pass
    return {}


def generate_tactical_summary(match_dashboard: dict[str, Any]) -> str:
    """Generate 1-2 paragraph tactical summary."""
    cache_key = f"summary_{id(match_dashboard)}"
    if cache_key in _CACHE:
        return _safe_str(_CACHE[cache_key].get("summary"))
    ai_result = _call_ai_tactical_analysis(match_dashboard)
    if ai_result.get("summary"):
        _CACHE[cache_key] = ai_result
        return ai_result["summary"]
    fallback = _generate_fallback_analysis(match_dashboard)
    _CACHE[cache_key] = fallback
    return fallback["summary"]


def generate_team_strengths(match_dashboard: dict[str, Any]) -> dict[str, list[str]]:
    """Generate 3-5 strengths."""
    cache_key = f"strengths_{id(match_dashboard)}"
    if cache_key in _CACHE:
        return _CACHE[cache_key].get("strengths", {})
    ai_result = _call_ai_tactical_analysis(match_dashboard)
    if ai_result.get("strengths"):
        _CACHE[cache_key] = ai_result
        return ai_result["strengths"]
    fallback = _generate_fallback_analysis(match_dashboard)
    _CACHE[cache_key] = fallback
    return fallback["strengths"]


def generate_team_weaknesses(match_dashboard: dict[str, Any]) -> dict[str, list[str]]:
    """Generate 3-5 weaknesses."""
    cache_key = f"weaknesses_{id(match_dashboard)}"
    if cache_key in _CACHE:
        return _CACHE[cache_key].get("weaknesses", {})
    ai_result = _call_ai_tactical_analysis(match_dashboard)
    if ai_result.get("weaknesses"):
        _CACHE[cache_key] = ai_result
        return ai_result["weaknesses"]
    fallback = _generate_fallback_analysis(match_dashboard)
    _CACHE[cache_key] = fallback
    return fallback["weaknesses"]


def generate_coach_recommendations(match_dashboard: dict[str, Any]) -> dict[str, list[str]]:
    """Generate 3-5 actionable recommendations."""
    cache_key = f"recommendations_{id(match_dashboard)}"
    if cache_key in _CACHE:
        return _CACHE[cache_key].get("recommendations", {})
    ai_result = _call_ai_tactical_analysis(match_dashboard)
    if ai_result.get("recommendations"):
        _CACHE[cache_key] = ai_result
        return ai_result["recommendations"]
    fallback = _generate_fallback_analysis(match_dashboard)
    _CACHE[cache_key] = fallback
    return fallback["recommendations"]


def generate_match_verdict(match_dashboard: dict[str, Any]) -> dict:
    """Generate concise executive verdict."""
    cache_key = f"verdict_{id(match_dashboard)}"
    if cache_key in _CACHE:
        return _CACHE[cache_key].get("verdict", {})
    ai_result = _call_ai_tactical_analysis(match_dashboard)
    if ai_result.get("verdict"):
        _CACHE[cache_key] = ai_result
        return ai_result["verdict"]
    fallback = _generate_fallback_analysis(match_dashboard)
    _CACHE[cache_key] = fallback
    return fallback["verdict"]


def generate_full_tactical_analysis(match_dashboard: dict[str, Any]) -> dict[str, Any]:
    """Orchestrate all tactical analysis functions by calling each dedicated function."""
    cache_key = f"full_{id(match_dashboard)}"
    if cache_key in _CACHE:
        return dict(_CACHE[cache_key])

    result = {
        "summary": generate_tactical_summary(match_dashboard),
        "strengths": generate_team_strengths(match_dashboard),
        "weaknesses": generate_team_weaknesses(match_dashboard),
        "recommendations": generate_coach_recommendations(match_dashboard),
        "verdict": generate_match_verdict(match_dashboard),
    }

    _CACHE[cache_key] = result
    return dict(result)