
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

# 1. Revenue by product category
category_analysis = sales.groupby("Category").agg(
    Total_Revenue=("Net_Revenue", "sum"),
    Total_Transactions=("Transaction_ID", "nunique"),
    Total_Units=("Units", "sum")
).reset_index()

category_analysis = category_analysis.sort_values(
    "Total_Revenue", ascending=False
)

# 2. Revenue by city
city_analysis = sales.groupby("City").agg(
    Total_Revenue=("Net_Revenue", "sum"),
    Total_Transactions=("Transaction_ID", "nunique")
).reset_index()

city_analysis = city_analysis.sort_values(
    "Total_Revenue", ascending=False
)

# 3. Revenue by sales channel
channel_analysis = sales.groupby("Channel").agg(
    Total_Revenue=("Net_Revenue", "sum"),
    Total_Transactions=("Transaction_ID", "nunique")
).reset_index()

channel_analysis = channel_analysis.sort_values(
    "Total_Revenue", ascending=False
)

# Save reports
category_analysis.to_csv(
    os.path.join(REPORT_DIR, "category_analysis.csv"),
    index=False
)

city_analysis.to_csv(
    os.path.join(REPORT_DIR, "city_analysis.csv"),
    index=False
)

channel_analysis.to_csv(
    os.path.join(REPORT_DIR, "channel_analysis.csv"),
    index=False
)

print("\nCATEGORY ANALYSIS")
print(category_analysis.to_string(index=False))

print("\nCITY ANALYSIS")
print(city_analysis.to_string(index=False))

print("\nCHANNEL ANALYSIS")
print(channel_analysis.to_string(index=False))

print("\nReports saved successfully!")
