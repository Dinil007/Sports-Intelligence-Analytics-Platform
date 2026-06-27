import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import joblib
import pandas as pd

from auth.streamlit_auth import is_authenticated
if not is_authenticated():
    st.stop()

# Page Config handled by central entry point app.py

st.title("🏥 Injury Risk Prediction")

# Load trained model
model = joblib.load("models/injury_prediction_model.pkl")

st.markdown("Enter athlete metrics below:")

training_load = st.slider("Training Load", 0, 150, 80)
sprint_count = st.slider("Sprint Count", 0, 100, 30)
distance_covered = st.slider("Distance Covered (km)", 0.0, 20.0, 10.0)
heart_rate = st.slider("Heart Rate", 60, 220, 140)
recovery_score = st.slider("Recovery Score", 0, 100, 70)
fatigue_score = st.slider("Fatigue Score", 0, 100, 40)

if st.button("Predict Injury Risk"):

    input_df = pd.DataFrame([{
        "training_load": training_load,
        "sprint_count": sprint_count,
        "distance_covered": distance_covered,
        "heart_rate": heart_rate,
        "recovery_score": recovery_score,
        "fatigue_score": fatigue_score
    }])

    prediction = model.predict(input_df)[0]

    if prediction == "High":
        st.error("🔴 High Injury Risk")
    elif prediction == "Medium":
        st.warning("🟡 Medium Injury Risk")
    else:
        st.success("🟢 Low Injury Risk")