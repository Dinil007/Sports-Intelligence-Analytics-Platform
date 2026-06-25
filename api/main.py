from pathlib import Path
import os

import joblib
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine

# -------------------------------------------------------
# Load environment variables
# -------------------------------------------------------

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

# -------------------------------------------------------
# Load ML model (optional)
# -------------------------------------------------------

model = None
model_path = Path(__file__).resolve().parent.parent / "models" / "match_outcome_model.pkl"

if model_path.exists():
    model = joblib.load(model_path)

# -------------------------------------------------------
# FastAPI
# -------------------------------------------------------

app = FastAPI(
    title="Sports Intelligence & Analytics Platform API",
    version="2.0.0",
)

# -------------------------------------------------------
# Root
# -------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Sports Intelligence & Analytics Platform API",
        "status": "running",
    }

# -------------------------------------------------------
# Players
# -------------------------------------------------------

@app.get("/players")
def players():

    query = """
    SELECT *
    FROM vw_sporta_score
    ORDER BY sporta_score DESC
    LIMIT 100;
    """

    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

# -------------------------------------------------------
# Teams
# -------------------------------------------------------

@app.get("/teams")
def teams():

    query = """
    SELECT *
    FROM vw_team_performance
    ORDER BY goals DESC;
    """

    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

# -------------------------------------------------------
# Scouting
# -------------------------------------------------------

@app.get("/scouting")
def scouting():

    query = """
    SELECT *
    FROM vw_scouting
    ORDER BY sporta_score DESC
    LIMIT 100;
    """

    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

# -------------------------------------------------------
# Top Scorers
# -------------------------------------------------------

@app.get("/top-scorers")
def top_scorers():

    query = """
    SELECT *
    FROM vw_top_goal_scorers
    ORDER BY goals DESC
    LIMIT 50;
    """

    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

# -------------------------------------------------------
# xG Analysis
# -------------------------------------------------------

@app.get("/xg-analysis")
def xg_analysis():

    query = """
    SELECT *
    FROM vw_xg_analysis
    ORDER BY expected_goals DESC
    LIMIT 50;
    """

    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

# -------------------------------------------------------
# Match Prediction (Demo)
# -------------------------------------------------------

class MatchPredictionRequest(BaseModel):
    home_score: int
    away_score: int


@app.post("/predict-match")
def predict_match(request: MatchPredictionRequest):

    if model is None:
        return {
            "error": "Model file not found. Train and save the model first."
        }

    prediction = model.predict(
        [[request.home_score, request.away_score]]
    )[0]

    if prediction == 1:
        result = "Home Win"
    elif prediction == 0:
        result = "Draw"
    else:
        result = "Away Win"

    return {
        "prediction": result,
        "home_score_input": request.home_score,
        "away_score_input": request.away_score,
    }

