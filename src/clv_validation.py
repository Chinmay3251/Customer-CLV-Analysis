
import pandas as pd
import os

from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Data")
REPORT_DIR = os.path.join(BASE_DIR, "Reports")

os.makedirs(REPORT_DIR, exist_ok=True)

# Load sales data
sales = pd.read_csv(
    os.path.join(DATA_DIR, "cleaned_sales.csv")
)

sales["Date"] = pd.to_datetime(sales["Date"])

# Define validation period
max_date = sales["Date"].max()
validation_start = max_date - pd.DateOffset(months=6)

# Split historical and validation data
historical = sales[
    sales["Date"] < validation_start
].copy()

future = sales[
    sales["Date"] >= validation_start
].copy()

# Historical customer revenue
historical_revenue = historical.groupby(
    "Customer_ID"
)["Net_Revenue"].sum().reset_index()

historical_revenue.rename(
    columns={"Net_Revenue": "Historical_Revenue"},
    inplace=True
)

# Actual validation-period revenue
actual_revenue = future.groupby(
    "Customer_ID"
)["Net_Revenue"].sum().reset_index()

actual_revenue.rename(
    columns={"Net_Revenue": "Actual_Future_Revenue"},
    inplace=True
)

# Keep all customers in the dataset
all_customers = sales[["Customer_ID"]].drop_duplicates()

validation = all_customers.merge(
    historical_revenue,
    on="Customer_ID",
    how="left"
)

validation = validation.merge(
    actual_revenue,
    on="Customer_ID",
    how="left"
)

validation = validation.fillna(0)

# Baseline prediction:
# Predict future revenue using historical revenue.
# Calculate the historical observation period in days
historical_days = (validation_start - sales["Date"].min()).days

# Estimate revenue for an equivalent six-month period
six_month_days = 182.5

validation["Predicted_Future_Revenue"] = (
    validation["Historical_Revenue"] / historical_days
) * six_month_days

# Calculate evaluation metrics
mae = mean_absolute_error(
    validation["Actual_Future_Revenue"],
    validation["Predicted_Future_Revenue"]
)

rmse = np.sqrt(
    mean_squared_error(
        validation["Actual_Future_Revenue"],
        validation["Predicted_Future_Revenue"]
    )
)

# Save customer-level predictions
validation.to_csv(
    os.path.join(REPORT_DIR, "clv_validation_results.csv"),
    index=False
)

# Print results
print("\n========== CLV BASELINE MODEL ==========")

print("Total customers:", len(validation))

print(
    "Average historical revenue:",
    round(validation["Historical_Revenue"].mean(), 2)
)

print(
    "Average actual future revenue:",
    round(validation["Actual_Future_Revenue"].mean(), 2)
)

print(
    "Average predicted future revenue:",
    round(validation["Predicted_Future_Revenue"].mean(), 2)
)

print("\n========== MODEL EVALUATION ==========")

print(f"MAE: ₹{mae:.2f}")
print(f"RMSE: ₹{rmse:.2f}")

print("\nResults saved successfully!")
