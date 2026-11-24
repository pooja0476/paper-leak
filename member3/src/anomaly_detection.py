import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(features):

    # Select numerical features for the model
    columns = [
        "average_score",
        "score_std",
        "top_scorer_percentage"
    ]

    X = features[columns].fillna(0)

    # Create Isolation Forest model
    model = IsolationForest(
        contamination=0.2,
        random_state=42
    )

    # Train and predict
    features["anomaly_prediction"] = model.fit_predict(X)

    # Generate anomaly scores
    features["anomaly_score"] = model.decision_function(X)

    # -1 means unusual, 1 means normal
    features["anomaly_flag"] = (
        features["anomaly_prediction"] == -1
    )

    return features


if __name__ == "__main__":

    features = pd.read_csv(
        "member3/outputs/centre_metrics.csv"
    )

    results = detect_anomalies(features)

    print("Anomaly Detection Results:")
    print(results)

    results.to_csv(
        "member3/outputs/anomaly_results.csv",
        index=False
    )

    print("\nAnomaly results saved successfully!")