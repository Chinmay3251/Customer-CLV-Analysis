
import pandas as pd
import os

# --------------------------------
# 1. Set project paths
# --------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORT_DIR, exist_ok=True)

# --------------------------------
# 2. Load cleaned datasets
# --------------------------------

sales = pd.read_csv(
    os.path.join(DATA_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Data\\cleaned_sales.csv")
)

customers = pd.read_csv(
    os.path.join(DATA_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Data\\cleaned_customers.csv")
)

# Convert dates
sales["Date"] = pd.to_datetime(sales["Date"])
customers["First_Purchase_Date"] = pd.to_datetime(
    customers["First_Purchase_Date"]
)
customers["Last_Purchase_Date"] = pd.to_datetime(
    customers["Last_Purchase_Date"]
)

print("Datasets loaded successfully!")

# --------------------------------
# 3. Transaction metrics
# --------------------------------

total_transactions = len(sales)

unique_customers = sales["Customer_ID"].nunique()

gross_revenue = sales["Gross_Revenue"].sum()

discounted_revenue = sales["Transaction_Revenue"].sum()

realized_revenue = sales["Net_Revenue"].sum()

returned_transactions = (sales["Return_Flag"] == 1).sum()

return_rate = (
    returned_transactions / total_transactions
) * 100 if total_transactions else 0

average_transaction_value = (
    realized_revenue / total_transactions
) if total_transactions else 0

# --------------------------------
# 4. Customer metrics
# --------------------------------

total_customers = customers["Customer_ID"].nunique()

churned_customers = (customers["Churned"] == 1).sum()

active_customers = total_customers - churned_customers

churn_rate = (
    churned_customers / total_customers
) * 100 if total_customers else 0

average_revenue_per_customer = (
    realized_revenue / total_customers
) if total_customers else 0

# --------------------------------
# 5. Date metrics
# --------------------------------

first_transaction_date = sales["Date"].min()

last_transaction_date = sales["Date"].max()

# --------------------------------
# 6. Create baseline report
# --------------------------------

metrics = {
    "Metric": [
        "Total Transactions",
        "Total Customers",
        "Unique Sales Customers",
        "Gross Revenue",
        "Revenue After Discounts",
        "Realized Revenue After Returns",
        "Returned Transactions",
        "Return Rate (%)",
        "Average Transaction Value",
        "Active Customers",
        "Churned Customers",
        "Churn Rate (%)",
        "Average Revenue Per Customer",
        "First Transaction Date",
        "Last Transaction Date"
    ],

    "Value": [
        total_transactions,
        total_customers,
        unique_customers,
        round(gross_revenue, 2),
        round(discounted_revenue, 2),
        round(realized_revenue, 2),
        returned_transactions,
        round(return_rate, 2),
        round(average_transaction_value, 2),
        active_customers,
        churned_customers,
        round(churn_rate, 2),
        round(average_revenue_per_customer, 2),
        first_transaction_date.date(),
        last_transaction_date.date()
    ]
}

baseline_report = pd.DataFrame(metrics)

# --------------------------------
# 7. Save report
# --------------------------------

output_path = os.path.join(
    REPORT_DIR,
    "baseline_metrics.csv"
)

baseline_report.to_csv(output_path, index=False)

# --------------------------------
# 8. Display results
# --------------------------------

print("\n========== BASELINE METRICS ==========\n")

print(baseline_report.to_string(index=False))

print("\n======================================")

print("\nReport saved successfully!")
print(output_path)
