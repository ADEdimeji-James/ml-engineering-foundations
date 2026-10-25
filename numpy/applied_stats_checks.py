
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = (
    REPO_ROOT
    / "pandas"
    / "retail_orders_analysis"
    / "data"
    / "day3_retail_orders.csv"
)

df = pd.read_csv(DATA_PATH)

# Separate completed and cancelled orders.
completed = df.loc[
    df["order_status"] == "Completed", "discount_pct"
].dropna().to_numpy(dtype=float)

cancelled = df.loc[
    df["order_status"] == "Cancelled", "discount_pct"
].dropna().to_numpy(dtype=float)

# Compare descriptive statistics using NumPy.
for name, values in [
    ("Completed", completed),
    ("Cancelled", cancelled),
]:
    print(f"\n{name} orders:")
    print(f"Sample size: {len(values)}")
    print(f"Mean discount: {np.mean(values):.2f}%")
    print(f"Median discount: {np.median(values):.2f}%")
    print(f"Standard deviation: {np.std(values, ddof=1):.2f}")

# Welch's independent two-sample t-test.
result = ttest_ind(
    completed,
    cancelled,
    equal_var=False,
)

print("\nWelch's t-test")
print(f"T-statistic: {result.statistic:.4f}")
print(f"P-value: {result.pvalue:.4f}")
