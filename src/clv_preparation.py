
import pandas as pd
import os

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Data")
REPORT_DIR = os.path.join(BASE_DIR, "Reports")

os.makedirs(REPORT_DIR, exist_ok=True)

# Load sales data
sales = pd.read_csv(
    os.path.join(DATA_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Data\\cleaned_sales.csv")
)

# Convert date column
sales["Date"] = pd.to_datetime(sales["Date"])

# Customer-level CLV preparation
customer_clv = sales.groupby("Customer_ID").agg(
    Total_Revenue=("Net_Revenue", "sum"),
    Total_Transactions=("Transaction_ID", "nunique"),
    Total_Units=("Units", "sum"),
    First_Purchase=("Date", "min"),
    Last_Purchase=("Date", "max")
).reset_index()

# Calculate average transaction value
customer_clv["Average_Transaction_Value"] = (
    customer_clv["Total_Revenue"] /
    customer_clv["Total_Transactions"]
)

# Calculate customer activity period
customer_clv["Customer_Age_Days"] = (
    customer_clv["Last_Purchase"] -
    customer_clv["First_Purchase"]
).dt.days

# Calculate historical average monthly revenue
customer_clv["Monthly_Revenue"] = (
    customer_clv["Total_Revenue"] /
    (customer_clv["Customer_Age_Days"].clip(lower=30) / 30)
)

# Merge K-Means business segments
segments = pd.read_csv(
    os.path.join(REPORT_DIR, "kmeans_customer_segments.csv")
)

customer_clv = customer_clv.merge(
    segments[["Customer_ID", "Cluster", "Business_Segment"]],
    on="Customer_ID",
    how="left"
)

# Sort customers by revenue
customer_clv = customer_clv.sort_values(
    "Total_Revenue",
    ascending=False
)

# Save customer-level report
output_path = os.path.join(
    REPORT_DIR,
    "customer_clv_baseline.csv"
)

customer_clv.to_csv(output_path, index=False)

# Overall summary
print("\n========== CUSTOMER CLV BASELINE ==========")

print("Total customers:", customer_clv["Customer_ID"].nunique())

print(
    "Total historical revenue:",
    round(customer_clv["Total_Revenue"].sum(), 2)
)

print(
    "Average customer revenue:",
    round(customer_clv["Total_Revenue"].mean(), 2)
)

print(
    "Average transaction value:",
    round(customer_clv["Average_Transaction_Value"].mean(), 2)
)

print(
    "Average customer activity period:",
    round(customer_clv["Customer_Age_Days"].mean(), 2),
    "days"
)

print("\n========== TOP 10 CUSTOMERS ==========")

print(
    customer_clv[
        ["Customer_ID", "Total_Revenue",
         "Total_Transactions", "Business_Segment"]
    ].head(10).to_string(index=False)
)

print("\nReport saved successfully!")
print(output_path)
