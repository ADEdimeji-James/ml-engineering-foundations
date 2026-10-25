
from pathlib import Path

import pandas as pd


# Find the repository root from this script's location.
REPO_ROOT = Path(__file__).resolve().parents[2]

# Reuse the original retail dataset from Day 3.
DATA_PATH = (
    REPO_ROOT
    / "pandas"
    / "retail_orders_analysis"
    / "data"
    / "day3_retail_orders.csv"
)


def main():
    """Inspect the retail dataset before ML modeling."""

    # Load the dataset into a Pandas DataFrame.
    df = pd.read_csv(DATA_PATH)

    # Check the number of rows and columns.
    print("Dataset shape:", df.shape)

    # Identify all available variables.
    print("\nColumn names:")
    print(df.columns.tolist())

    # Preview the first five records.
    print("\nFirst five rows:")
    print(df.head().to_string(index=False))

    # Inspect the data types.
    print("\nData types:")
    print(df.dtypes)

    # Check for missing values.
    print("\nMissing values:")
    print(df.isna().sum())

    # Examine how many orders belong to each status.
    print("\nOrder status distribution:")
    print(df["order_status"].value_counts(dropna=False))

    # Examine each status as a percentage of all orders.
    print("\nOrder status percentages:")
    status_percentages = (
        df["order_status"]
        .value_counts(normalize=True, dropna=False)
        .mul(100)
        .round(2)
    )
    print(status_percentages)



if __name__ == "__main__":
    main()
