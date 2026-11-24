import pandas as pd

def compare_historical_performance():

    historical = pd.read_csv(
        "member3/data/historical_scores.csv"
    )

    current = pd.read_csv(
        "member3/data/current_scores.csv"
    )

    # Calculate previous average marks
    old_avg = historical.groupby("centre_id")["score"].mean()

    # Calculate current average marks
    new_avg = current.groupby("centre_id")["score"].mean()

    # Combine both results
    comparison = pd.DataFrame({
        "historical_average": old_avg,
        "current_average": new_avg
    }).reset_index()

    # Calculate change in marks
    comparison["score_change"] = (
        comparison["current_average"] -
        comparison["historical_average"]
    )

    # Flag unusually large changes
    comparison["unusual_change"] = (
        comparison["score_change"].abs() >= 15
    )

    return comparison


if __name__ == "__main__":

    results = compare_historical_performance()

    print("Historical Performance Comparison:")
    print(results)

    results.to_csv(
        "member3/outputs/historical_comparison.csv",
        index=False
    )

    print("\nHistorical comparison saved successfully!")
    # Repeated unusual pattern analysis

def detect_repeated_patterns():

    historical = pd.read_csv(
        "member3/data/historical_scores.csv"
    )

    current = pd.read_csv(
        "member3/data/current_scores.csv"
    )

    all_data = pd.concat([historical, current])

    exam_averages = all_data.groupby(
        ["centre_id", "exam_id"]
    )["score"].mean().reset_index()

    exam_averages = exam_averages.sort_values(
        ["centre_id", "exam_id"]
    )

    exam_averages["score_change"] = (
        exam_averages.groupby("centre_id")["score"].diff()
    )

    exam_averages["unusual_change"] = (
        exam_averages["score_change"].abs() >= 15
    )

    repeated = exam_averages.groupby("centre_id")[
        "unusual_change"
    ].sum().reset_index()

    repeated["repeated_unusual_pattern"] = (
        repeated["unusual_change"] >= 2
    )

    repeated.to_csv(
        "member3/outputs/repeated_patterns.csv",
        index=False
    )

    print("\nRepeated Pattern Analysis:")
    print(repeated)

    print("\nRepeated pattern results saved!")


detect_repeated_patterns()