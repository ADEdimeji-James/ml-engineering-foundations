# Retail Orders Data Analysis Using Python and Pandas

## Project Overview

This project demonstrates an end-to-end data analysis workflow using Python and Pandas.

The objective is to transform raw retail transaction data into clean, structured information and generate insights about sales performance across product categories, regions, and months.

## Dataset

The dataset contains 81 raw records covering retail orders from July to September 2026.

The dataset includes order information such as:

- Order ID and customer ID
- Order date and region
- Product and category
- Quantity and unit price
- Discount percentage
- Payment method and order status

This is a synthetic dataset created for educational purposes.

## Tools and Technologies

- Python
- Pandas
- Visual Studio Code
- Git and GitHub

## Analysis Workflow

1. **Data Loading:** Imported the raw CSV dataset using Pandas.
2. **Data Inspection:** Examined dataset dimensions, column types, missing values, and duplicate records.
3. **Data Cleaning:** Removed duplicate records, handled missing discount values, standardized categorical text, and converted dates into datetime objects.
4. **Feature Engineering:** Created gross revenue, discount amount, net revenue, and order month columns.
5. **Business Analysis:** Analyzed completed-order revenue by product category, region, and month.
6. **Data Export:** Saved the prepared dataset and summarized revenue reports as CSV files.

## Data Cleaning Decisions

- Removed one exact duplicate record.
- Replaced two missing discount values with zero, assuming no discount was applied.
- Preserved the missing customer ID rather than inventing a customer identifier.
- Converted the order date column to a datetime format.
- Standardized inconsistent capitalization in selected categorical columns.

## Key Findings

- **Furniture** generated the highest completed-order revenue, totaling 8,944.00.
- **Lagos** generated the highest completed-order revenue among regions, totaling 5,905.25.
- Revenue reporting was restricted to completed orders to avoid including cancelled or pending transactions.

Revenue figures are presented without a currency symbol because the source dataset does not specify a currency.

## How to Run

From the repository root, with Python and Pandas installed:

```bash
python pandas/retail_orders_analysis/analysis.py
```

The script inspects the dataset, cleans the data, engineers features, performs sales analysis, and exports the results.

## Project Outputs

The `outputs/` directory contains:

- `cleaned_retail_orders.csv`
- `category_revenue.csv`
- `region_revenue.csv`

## Potential Improvements

- Create revenue visualizations.
- Add automated data-quality checks.
- Investigate average order value and customer purchasing patterns.
- Expand the analysis to evaluate profitability when product cost data is available.
