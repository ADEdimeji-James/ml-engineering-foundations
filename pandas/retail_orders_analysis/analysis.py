
from pathlib import Path

import pandas as pd


# STEP 1: Locate the dataset.
# __file__ refers to the current Python script.
# .parent refers to the folder containing this script.
DATA_PATH = Path(__file__).parent / "data" / "day3_retail_orders.csv"


def load_data(file_path):
    """
    Read a CSV file and return a Pandas DataFrame.
    """
    df = pd.read_csv(file_path)
    return df


def inspect_data(df):
    """
    Examine the dataset before cleaning or analyzing it.
    """

    # Number of rows and columns
    print("\n--- DATASET SHAPE ---")
    print(df.shape)

    # Display the first five records
    print("\n--- FIRST 5 ROWS ---")
    print(df.head())

    # Display all column names
    print("\n--- COLUMN NAMES ---")
    print(df.columns.tolist())

    # Check the data type of each column
    print("\n--- DATA TYPES ---")
    print(df.dtypes)

    # Count missing values in each column
    print("\n--- MISSING VALUES ---")
    print(df.isna().sum())

    # Count completely duplicated rows
    print("\n--- DUPLICATE ROWS ---")
    print(df.duplicated().sum())


def clean_data(df):
    """
    Clean the retail orders dataset and return
    a cleaned DataFrame.
    """

    # STEP 1: Create a copy of the original data
    df = df.copy()

    # STEP 2: Remove exact duplicate rows
    df = df.drop_duplicates()

    # STEP 3: Handle missing discount values
    # Assumption: Missing discounts represent 0%.
    df["discount_pct"] = df["discount_pct"].fillna(0)

    # STEP 4: Convert order_date from text to datetime
    df["order_date"] = pd.to_datetime(df["order_date"])

    # STEP 5: Standardize inconsistent text
    df["region"] = df["region"].str.strip().str.title()

    df["category"] = df["category"].str.strip().str.title()

    df["payment_method"] = df["payment_method"].str.strip().str.title()

    return df


def engineer_features(df):
    """
    Create new columns useful for business analysis.
    """

    # Work on a copy to preserve our cleaned dataset
    df = df.copy()

    # STEP 1: Calculate revenue before discounts
    df["gross_revenue"] = (
        df["quantity"] * df["unit_price"]
    )

    # STEP 2: Calculate how much money was discounted
    df["discount_amount"] = (
        df["gross_revenue"] * df["discount_pct"] / 100
    )

    # STEP 3: Calculate revenue after discounts
    df["net_revenue"] = (
        df["gross_revenue"] - df["discount_amount"]
    )

    # STEP 4: Extract the month from the order date
    df["order_month"] = (
        df["order_date"].dt.to_period("M").astype(str)
    )

    return df


def analyze_sales(df):
    """
    Analyze revenue from completed retail orders.
    """

    # STEP 1: Keep only completed orders
    completed_df = df[
        df["order_status"] == "Completed"
    ].copy()

    # STEP 2: Calculate total completed sales revenue
    total_revenue = completed_df["net_revenue"].sum()

    print("\n========== SALES ANALYSIS ==========")

    print("\n--- TOTAL COMPLETED SALES REVENUE ---")
    print(round(total_revenue, 2))

    # STEP 3: Revenue by product category
    category_revenue = (
        completed_df.groupby("category")["net_revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n--- REVENUE BY CATEGORY ---")
    print(category_revenue)

    # STEP 4: Revenue by region
    region_revenue = (
        completed_df.groupby("region")["net_revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n--- REVENUE BY REGION ---")
    print(region_revenue)

    # STEP 5: Monthly revenue
    monthly_revenue = (
        completed_df.groupby("order_month")["net_revenue"]
        .sum()
        .sort_index()
    )

    print("\n--- MONTHLY REVENUE ---")
    print(monthly_revenue)

    # STEP 6: Number of completed orders
    print("\n--- TOTAL COMPLETED ORDERS ---")
    print(len(completed_df))


def export_results(df):
    """
    Export the prepared dataset and summary reports.
    """

    # Create an output directory beside this script
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save all cleaned, feature-engineered records
    df.to_csv(
        output_dir / "cleaned_retail_orders.csv",
        index=False
    )

    # Keep only completed orders for sales reports
    completed_df = df[
        df["order_status"] == "Completed"
    ].copy()

    # Create a category summary
    category_summary = (
        completed_df.groupby("category", as_index=False)
        .agg(
            total_revenue=("net_revenue", "sum"),
            order_count=("order_id", "nunique")
        )
        .sort_values("total_revenue", ascending=False)
    )

    # Create a region summary
    region_summary = (
        completed_df.groupby("region", as_index=False)
        .agg(
            total_revenue=("net_revenue", "sum"),
            order_count=("order_id", "nunique")
        )
        .sort_values("total_revenue", ascending=False)
    )

    # Export the summaries
    category_summary.to_csv(
        output_dir / "category_revenue.csv",
        index=False
    )

    region_summary.to_csv(
        output_dir / "region_revenue.csv",
        index=False
    )

    print("\n========== EXPORT COMPLETE ==========")
    print(f"Results saved to: {output_dir}")



def main():

    # STEP 1: Load data
    df = load_data(DATA_PATH)

    print("\n========== RAW DATA ==========")
    inspect_data(df)

    # STEP 2: Clean data
    cleaned_df = clean_data(df)

    print("\n========== CLEANED DATA ==========")
    inspect_data(cleaned_df)

    # STEP 3: Engineer new features
    featured_df = engineer_features(cleaned_df)

    print("\n========== FEATURE ENGINEERING ==========")

    # Display our new calculated columns
    columns_to_display = [
        "order_id",
        "quantity",
        "unit_price",
        "discount_pct",
        "gross_revenue",
        "discount_amount",
        "net_revenue",
        "order_month",
    ]

    print(featured_df[columns_to_display].head())

    print("\n--- UPDATED DATASET SHAPE ---")
    print(featured_df.shape)

    # STEP 4: Perform business analysis
    analyze_sales(featured_df)


    # STEP 5: Export prepared data and business reports
    export_results(featured_df)

if __name__ == "__main__":
    main()
