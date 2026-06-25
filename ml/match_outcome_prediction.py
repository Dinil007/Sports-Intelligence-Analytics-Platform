import os
from pathlib import Path

import joblib
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

# ---------------------------------------------------
# Load environment variables
# ---------------------------------------------------

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

# ---------------------------------------------------
# Load data
# ---------------------------------------------------

query = """
SELECT
    match_id,
    home_score,
    away_score
FROM matches_raw
WHERE home_score IS NOT NULL
  AND away_score IS NOT NULL;
"""

df = pd.read_sql(query, engine)

print(f"✅ Loaded {len(df)} matches")

# ---------------------------------------------------
# Create target variable
# 1 = Home Win
# 0 = Draw
# -1 = Away Win
# ---------------------------------------------------

def get_result(row):
    if row["home_score"] > row["away_score"]:
        return 1
    elif row["home_score"] < row["away_score"]:
        return -1
    else:
        return 0


df["result"] = df.apply(get_result, axis=1)

# ---------------------------------------------------
# Features and target
# ---------------------------------------------------

X = df[["home_score", "away_score"]]
y = df["result"]

# ---------------------------------------------------
# Train/Test Split
# ---------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ---------------------------------------------------
# Train Model
# ---------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# ---------------------------------------------------
# Evaluate
# ---------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n==============================")
print(f"✅ Accuracy: {accuracy:.4f}")
print("==============================\n")

print(classification_report(y_test, predictions))

# ---------------------------------------------------
# Save model
# ---------------------------------------------------

models_dir = Path("models")
models_dir.mkdir(exist_ok=True)

model_path = models_dir / "match_outcome_model.pkl"

joblib.dump(model, model_path)

print(f"✅ Model saved successfully: {model_path}")