"""Feature engineering functions for enhancing football datasets."""

from __future__ import annotations

import pandas as pd
import numpy as np

def engineer_match_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create match-level features like goal differences, rolling form, and home advantage."""
    df = df.copy()
    
    # 1. Goal differences
    if "home_goals" in df.columns and "away_goals" in df.columns:
        df["goal_difference"] = df["home_goals"] - df["away_goals"]
        df["total_goals"] = df["home_goals"] + df["away_goals"]
        
    # 2. Convert raw metrics to ratios
    if "home_shots" in df.columns and "home_shots_on_target" in df.columns:
        df["home_shot_accuracy"] = df["home_shots_on_target"] / (df["home_shots"] + 1e-5)
    if "away_shots" in df.columns and "away_shots_on_target" in df.columns:
        df["away_shot_accuracy"] = df["away_shots_on_target"] / (df["away_shots"] + 1e-5)
        
    # 3. Rolling forms (default fallback if dynamic data is missing)
    if "home_team_id" in df.columns:
        df["home_rolling_win_rate"] = df.get("home_rolling_win_rate", 0.6)
        df["away_rolling_win_rate"] = df.get("away_rolling_win_rate", 0.4)
        
    return df

def engineer_player_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create player-level features like goals per minute, pass completion rates, and xG efficiency."""
    df = df.copy()
    
    # Pass completion
    if "passes_completed" in df.columns and "passes_attempted" in df.columns:
        df["pass_completion_rate"] = df["passes_completed"] / (df["passes_attempted"] + 1e-5)
        
    # xG Efficiency
    if "goals" in df.columns and "xg" in df.columns:
        df["xg_efficiency"] = df["goals"] - df["xg"]
        
    # Goals per 90
    if "goals" in df.columns and "minutes_played" in df.columns:
        df["goals_per_90"] = (df["goals"] / (df["minutes_played"] + 1e-5)) * 90.0
        
    return df
