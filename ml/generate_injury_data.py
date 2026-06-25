import random
import pandas as pd

players = [f"Player_{i}" for i in range(1, 1001)]

rows = []

for player in players:
    training_load = random.randint(50, 120)
    sprint_count = random.randint(10, 80)
    distance_covered = round(random.uniform(5.0, 15.0), 2)
    heart_rate = random.randint(110, 190)
    recovery_score = random.randint(20, 100)
    fatigue_score = random.randint(20, 100)

    # Simple rule-based label for training
    if (
        training_load > 100
        and recovery_score < 40
        and fatigue_score > 70
    ):
        injury_risk = "High"
    elif (
        training_load > 80
        or fatigue_score > 60
    ):
        injury_risk = "Medium"
    else:
        injury_risk = "Low"

    rows.append({
        "player_name": player,
        "training_load": training_load,
        "sprint_count": sprint_count,
        "distance_covered": distance_covered,
        "heart_rate": heart_rate,
        "recovery_score": recovery_score,
        "fatigue_score": fatigue_score,
        "injury_risk": injury_risk,
    })

df = pd.DataFrame(rows)

df.to_csv("data/processed/injury_training_data.csv", index=False)

print("✅ Generated injury_training_data.csv")
print(df.head())