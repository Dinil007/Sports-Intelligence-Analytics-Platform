import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

from database.db_connection import engine


def get_similar_players(player_name: str, top_n: int = 10):
    """
    Find players similar to the given player using cosine similarity.
    Supports partial and case-insensitive player name matching.
    """

    query = """
    SELECT
        player_name,
        sporta_score,
        shots,
        passes,
        carries,
        pressures,
        recoveries,
        dribbles,
        goals,
        total_xg
    FROM vw_scouting;
    """

    df = pd.read_sql(query, engine)

    if df.empty:
        return pd.DataFrame()

    # Fill missing numeric values
    numeric_columns = [
        "sporta_score",
        "shots",
        "passes",
        "carries",
        "pressures",
        "recoveries",
        "dribbles",
        "goals",
        "total_xg",
    ]

    df[numeric_columns] = df[numeric_columns].fillna(0)

    # Find matching player (partial + case insensitive)
    matches = df[
        df["player_name"]
        .astype(str)
        .str.lower()
        .str.contains(player_name.lower(), na=False)
    ]

    if matches.empty:
        print(f"❌ Player '{player_name}' not found.")
        return pd.DataFrame()

    # Use first matching player
    selected_index = matches.index[0]

    scaler = StandardScaler()
    features = scaler.fit_transform(df[numeric_columns])

    similarity_matrix = cosine_similarity(features)

    similarity_scores = similarity_matrix[selected_index]

    result = df.copy()
    result["similarity_score"] = similarity_scores

    # Remove the selected player
    result = result[result.index != selected_index]

    # Sort by similarity
    result = result.sort_values(
        by="similarity_score",
        ascending=False
    )

    return result[
        [
            "player_name",
            "similarity_score",
            "sporta_score",
            "goals",
            "total_xg",
        ]
    ].head(top_n)


# Test
if __name__ == "__main__":

    player = input("Enter player name: ")

    recommendations = get_similar_players(player)

    if recommendations.empty:
        print("No recommendations found.")
    else:
        print("\nTop Similar Players:\n")
        print(recommendations.to_string(index=False))