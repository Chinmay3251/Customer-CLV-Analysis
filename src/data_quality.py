
import pandas as pd
import numpy as np
import os

# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORT_DIR, exist_ok=True)

sales_path = os.path.join(DATA_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Data\\da_sales_transactions.csv")
customer_path = os.path.join(DATA_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Data\\da_customer_profiles.csv")


# ==========================================
# 2. LOAD DATASETS
# ==========================================

sales = pd.read_csv(sales_path)
customers = pd.read_csv(customer_path)

print("=" * 50)
print("DATA CLEANING STARTED")
print("=" * 50)

print("Sales shape:", sales.shape)
print("Customer shape:", customers.shape)


# ==========================================
# 3. STANDARDIZE COLUMN NAMES
# ==========================================

sales.columns = sales.columns.str.strip()
customers.columns = customers.columns.str.strip()

# Remove unnecessary spaces from text values

for df in [sales, customers]:
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()


# ==========================================
# 4. CHECK MISSING VALUES
# ==========================================

print("\nSALES MISSING VALUES")
print(sales.isnull().sum())

print("\nCUSTOMER MISSING VALUES")
print(customers.isnull().sum())


# ==========================================
# 5. CHECK DUPLICATES
# ==========================================

print("\nDUPLICATE RECORDS")

print("Sales duplicates:", sales.duplicated().sum())
print("Customer duplicates:", customers.duplicated().sum())

# Remove exact duplicate rows

sales = sales.drop_duplicates().copy()
customers = customers.drop_duplicates().copy()

# Check duplicate IDs separately

print(
    "Duplicate transaction IDs:",
    sales["Transaction_ID"].duplicated().sum()
)

print(
    "Duplicate customer IDs:",
    customers["Customer_ID"].duplicated().sum()
)


# ==========================================
# 6. CONVERT DATA TYPES
# ==========================================

# Convert sales date

sales["Date"] = pd.to_datetime(
    sales["Date"],
    errors="coerce"
)

# Convert customer dates

customers["First_Purchase_Date"] = pd.to_datetime(
    customers["First_Purchase_Date"],
    errors="coerce"
)

customers["Last_Purchase_Date"] = pd.to_datetime(
    customers["Last_Purchase_Date"],
    errors="coerce"
)

# Convert numeric columns

sales_numeric = [
    "Units",
    "Unit_Price",
    "Discount_Pct",
    "Return_Flag"
]

customer_numeric = [
    "Total_Orders",
    "Total_Revenue",
    "Churned"
]

for col in sales_numeric:
    sales[col] = pd.to_numeric(
        sales[col],
        errors="coerce"
    )

for col in customer_numeric:
    customers[col] = pd.to_numeric(
        customers[col],
        errors="coerce"
    )


# ==========================================
# 7. VALIDATE VALUES
# ==========================================

print("\nINVALID VALUE CHECKS")

print(
    "Invalid sales dates:",
    sales["Date"].isna().sum()
)

print(
    "Invalid customer first purchase dates:",
    customers["First_Purchase_Date"].isna().sum()
)

print(
    "Invalid customer last purchase dates:",
    customers["Last_Purchase_Date"].isna().sum()
)

print(
    "Invalid units:",
    (sales["Units"] <= 0).sum()
)

print(
    "Invalid unit prices:",
    (sales["Unit_Price"] < 0).sum()
)

print(
    "Invalid discounts:",
    (~sales["Discount_Pct"].between(0, 100)).sum()
)

print(
    "Invalid return flags:",
    (~sales["Return_Flag"].isin([0, 1])).sum()
)

print(
    "Invalid churn flags:",
    (~customers["Churned"].isin([0, 1])).sum()
)

print(
    "Invalid order counts:",
    (customers["Total_Orders"] < 0).sum()
)

print(
    "Invalid customer revenue:",
    (customers["Total_Revenue"] < 0).sum()
)

# Check date consistency

invalid_date_order = (
    customers["First_Purchase_Date"]
    > customers["Last_Purchase_Date"]
).sum()

print("Invalid customer date sequences:", invalid_date_order)


# ==========================================
# 8. CHECK CUSTOMER ID RELATIONSHIPS
# ==========================================

sales_customer_ids = set(sales["Customer_ID"].dropna())

profile_customer_ids = set(customers["Customer_ID"].dropna())

matched_ids = sales_customer_ids.intersection(
    profile_customer_ids
)

unmatched_sales_ids = sales_customer_ids - profile_customer_ids

unmatched_profile_ids = profile_customer_ids - sales_customer_ids

print("\nCUSTOMER ID VALIDATION")

print("Unique sales customers:", len(sales_customer_ids))
print("Unique profile customers:", len(profile_customer_ids))
print("Matched customers:", len(matched_ids))
print("Unmatched sales customers:", len(unmatched_sales_ids))
print("Unmatched profile customers:", len(unmatched_profile_ids))


# ==========================================
# 9. CALCULATE TRANSACTION REVENUE
# ==========================================

# Revenue after discount

sales["Gross_Revenue"] = (
    sales["Units"] * sales["Unit_Price"]
)

sales["Discount_Amount"] = (
    sales["Gross_Revenue"]
    * sales["Discount_Pct"] / 100
)

sales["Transaction_Revenue"] = (
    sales["Gross_Revenue"]
    - sales["Discount_Amount"]
)

# Exclude returned transactions from realized revenue

sales["Net_Revenue"] = np.where(
    sales["Return_Flag"] == 0,
    sales["Transaction_Revenue"],
    0
)

print("\nREVENUE SUMMARY")

print(
    "Total Gross Revenue:",
    sales["Gross_Revenue"].sum()
)

print(
    "Total Transaction Revenue:",
    sales["Transaction_Revenue"].sum()
)

print(
    "Realized Revenue:",
    sales["Net_Revenue"].sum()
)


# ==========================================
# 10. FINAL MISSING VALUE CHECK
# ==========================================

print("\nFINAL MISSING VALUES")

print("Sales:")
print(sales.isnull().sum())

print("\nCustomers:")
print(customers.isnull().sum())


# ==========================================
# 11. EXPORT CLEANED DATASETS
# ==========================================

sales_output = os.path.join(
    DATA_DIR,
    "cleaned_sales.csv"
)

customer_output = os.path.join(
    DATA_DIR,
    "cleaned_customers.csv"
)

sales.to_csv(sales_output, index=False)

customers.to_csv(customer_output, index=False)


# ==========================================
# 12. GENERATE DATA QUALITY REPORT
# ==========================================

report = {
    "Dataset": [
        "Sales Transactions",
        "Customer Profiles"
    ],
    "Rows": [
        len(sales),
        len(customers)
    ],
    "Columns": [
        len(sales.columns),
        len(customers.columns)
    ],
    "Missing Values": [
        int(sales.isnull().sum().sum()),
        int(customers.isnull().sum().sum())
    ],
    "Duplicate Rows": [
        int(sales.duplicated().sum()),
        int(customers.duplicated().sum())
    ]
}

report_df = pd.DataFrame(report)

report_path = os.path.join(
    REPORT_DIR,
    "data_quality_report.csv"
)

report_df.to_csv(report_path, index=False)

print("\n" + "=" * 50)
print("DATA CLEANING COMPLETED")
print("=" * 50)

print("\nDATA QUALITY REPORT")
print(report_df)

print("\nGenerated files:")
print(sales_output)
print(customer_output)
print(report_path)
