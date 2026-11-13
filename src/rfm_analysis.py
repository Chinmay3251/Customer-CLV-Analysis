
import pandas as pd
import os

# ----------------------------------
# 1. Project paths
# ----------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "Data")
REPORT_DIR = os.path.join(BASE_DIR, "Reports")

os.makedirs(REPORT_DIR, exist_ok=True)

# ----------------------------------
# 2. Load cleaned sales data
# ----------------------------------

sales = pd.read_csv(
    os.path.join(DATA_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Data\\cleaned_sales.csv")
)

customers = pd.read_csv(
    os.path.join(DATA_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Data\\cleaned_customers.csv")
)

sales["Date"] = pd.to_datetime(sales["Date"])

print("Datasets loaded successfully!")

# ----------------------------------
# 3. Define analysis date
# ----------------------------------

# One day after the latest transaction
analysis_date = sales["Date"].max() + pd.Timedelta(days=1)

print("\nAnalysis date:", analysis_date.date())

# ----------------------------------
# 4. Calculate RFM metrics
# ----------------------------------

rfm = sales.groupby("Customer_ID").agg(
    Recency=("Date", lambda x: (analysis_date - x.max()).days),
    Frequency=("Transaction_ID", "nunique"),
    Monetary=("Net_Revenue", "sum")
).reset_index()

# ----------------------------------
# 5. Calculate RFM scores
# ----------------------------------

# Rank first to handle duplicate values
# and ensure five scoring groups.

rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

# All customers have the same frequency,
# so assign a neutral score of 3.

if rfm["Frequency"].nunique() == 1:
    rfm["F_Score"] = 3
else:
    rfm["F_Score"] = pd.qcut(
        rfm["Frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5]
    ).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Combined RFM score
rfm["RFM_Score"] = (
    rfm["R_Score"] +
    rfm["F_Score"] +
    rfm["M_Score"]
)

# ----------------------------------
# 6. Create five exploratory segments
# ----------------------------------

rfm["Customer_Segment"] = pd.qcut(
    rfm["RFM_Score"].rank(method="first"),
    5,
    labels=[
        "Low Value",
        "Below Average",
        "Average",
        "High Value",
        "Top Value"
    ]
)

# ----------------------------------
# 7. Merge customer profiles
# ----------------------------------

rfm = rfm.merge(
    customers[
        ["Customer_ID", "City", "Age_Band",
         "Gender", "Acquisition_Channel", "Churned"]
    ],
    on="Customer_ID",
    how="left"
)

# ----------------------------------
# 8. Segment-level analysis
# ----------------------------------

segment_summary = rfm.groupby(
    "Customer_Segment", observed=False
).agg(
    Customer_Count=("Customer_ID", "nunique"),
    Average_Recency=("Recency", "mean"),
    Average_Frequency=("Frequency", "mean"),
    Average_Monetary=("Monetary", "mean"),
    Total_Revenue=("Monetary", "sum"),
    Average_RFM_Score=("RFM_Score", "mean"),
    Churned_Customers=("Churned", "sum")
).reset_index()

segment_summary["Revenue_Percentage"] = (
    segment_summary["Total_Revenue"] /
    segment_summary["Total_Revenue"].sum()
) * 100

# ----------------------------------
# 9. Save reports
# ----------------------------------

rfm_path = os.path.join(
    REPORT_DIR, "customer_rfm.csv"
)

segment_path = os.path.join(
    REPORT_DIR, "rfm_segment_summary.csv"
)

rfm.to_csv(rfm_path, index=False)

segment_summary.to_csv(
    segment_path, index=False
)

# ----------------------------------
# 10. Display results
# ----------------------------------

print("\n========== CUSTOMER RFM ==========")

print(rfm.head(10).to_string(index=False))

print("\n========== RFM SEGMENT SUMMARY ==========")

print(segment_summary.round(2).to_string(index=False))

print("\nReports saved successfully!")
print(rfm_path)
print(segment_path)
