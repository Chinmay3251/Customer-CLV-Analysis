
import pandas as pd
import os

# Get the project directory automatically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

# Create reports folder if it doesn't exist
os.makedirs(REPORT_DIR, exist_ok=True)

# Load datasets
customers = pd.read_csv(
    os.path.join(DATA_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Data\\da_customer_profiles.csv")
)

sales = pd.read_csv(
    os.path.join(DATA_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Data\\da_sales_transactions.csv")
)

# Convert dates
customers["First_Purchase_Date"] = pd.to_datetime(
    customers["First_Purchase_Date"],
    errors="coerce"
)

customers["Last_Purchase_Date"] = pd.to_datetime(
    customers["Last_Purchase_Date"],
    errors="coerce"
)

sales["Date"] = pd.to_datetime(
    sales["Date"],
    errors="coerce"
)

# Identify inconsistent customer dates
date_issues = customers[
    customers["First_Purchase_Date"]
    > customers["Last_Purchase_Date"]
].copy()

print("Total date issues:", len(date_issues))

# Compare profile dates with available transaction dates
transaction_dates = sales.groupby("Customer_ID").agg(
    Sales_First_Date=("Date", "min"),
    Sales_Last_Date=("Date", "max")
).reset_index()

# Join transaction dates with affected customers
investigation = date_issues.merge(
    transaction_dates,
    on="Customer_ID",
    how="left"
)

print("\nDate inconsistency investigation:")

print(
    investigation[
        [
            "Customer_ID",
            "First_Purchase_Date",
            "Last_Purchase_Date",
            "Sales_First_Date",
            "Sales_Last_Date"
        ]
    ].to_string(index=False)
)

# Export results
output_path = os.path.join(
    REPORT_DIR,
    "date_inconsistencies.csv"
)

investigation.to_csv(output_path, index=False)

print("\nInvestigation report saved successfully!")
print("File location:", output_path)
