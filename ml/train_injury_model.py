import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Load the generated dataset
df = pd.read_csv("data/processed/injury_training_data.csv")

# Features
X = df[
    [
        "training_load",
        "sprint_count",
        "distance_covered",
        "heart_rate",
        "recovery_score",
        "fatigue_score",
    ]
]

# Target
y = df["injury_risk"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# Train Model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, predictions))
print("\nClassification Report:\n")
print(classification_report(y_test, predictions))

# Save Model
Path("models").mkdir(exist_ok=True)

joblib.dump(
    model,
    "models/injury_prediction_model.pkl"
)

print("\n✅ Model saved to models/injury_prediction_model.pkl")