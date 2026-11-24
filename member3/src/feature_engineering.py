import pandas as pd

def calculate_centre_features(data):

    features = data.groupby("centre_id").agg(
        average_score=("score", "mean"),
        score_std=("score", "std"),
        student_count=("student_id", "count")
    ).reset_index()

    # Calculate percentage of students scoring 90 or above
    top_scorers = data[data["score"] >= 90].groupby("centre_id").size()

    features["top_scorer_count"] = (
        features["centre_id"].map(top_scorers).fillna(0)
    )

    features["top_scorer_percentage"] = (
        features["top_scorer_count"] / features["student_count"] * 100
    )

    return features


if __name__ == "__main__":
    data = pd.read_csv("member3/data/current_scores.csv")

    features = calculate_centre_features(data)

    print("Centre-wise Performance:")
    print(features)

    features.to_csv("member3/outputs/centre_metrics.csv", index=False)

    print("\nCentre metrics saved successfully!")