
import pandas as pd
import os

# Dataset paths
sales_path = "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Data\\da_sales_transactions.csv"
customer_path = "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Data\\da_customer_profiles.csv"

# Check whether files exist
if not os.path.exists(sales_path):
    raise FileNotFoundError(f"Missing file: {sales_path}")

if not os.path.exists(customer_path):
    raise FileNotFoundError(f"Missing file: {customer_path}")

# Load datasets
sales = pd.read_csv(sales_path)
customers = pd.read_csv(customer_path)

# Display dataset information
print("\n========== SALES DATA ==========")
print("Shape:", sales.shape)
print("\nColumns:")
print(sales.columns.tolist())
print("\nFirst 5 rows:")
print(sales.head())
print("\nData types:")
print(sales.dtypes)
print("\nMissing values:")
print(sales.isnull().sum())

print("\n========== CUSTOMER DATA ==========")
print("Shape:", customers.shape)
print("\nColumns:")
print(customers.columns.tolist())
print("\nFirst 5 rows:")
print(customers.head())
print("\nData types:")
print(customers.dtypes)
print("\nMissing values:")
print(customers.isnull().sum())
