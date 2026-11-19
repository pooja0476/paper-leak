import pandas as pd

def load_and_clean_data(file_path):
    # Load CSV file
    data = pd.read_csv(file_path)

    # Remove duplicate records
    data = data.drop_duplicates()

    # Remove rows with missing values
    data = data.dropna()

    # Check valid marks
    data = data[
        (data["score"] >= 0) &
        (data["score"] <= data["max_score"])
    ]

    return data


if __name__ == "__main__":
    historical = load_and_clean_data(
        "member3/data/historical_scores.csv"
    )

    current = load_and_clean_data(
        "member3/data/current_scores.csv"
    )

    print("Historical data:")
    print(historical)

    print("\nCurrent data:")
    print(current)

    print("\nData cleaning completed!")