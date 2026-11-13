
import pandas as pd
import os

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Data")
REPORT_DIR = os.path.join(BASE_DIR, "Reports")

os.makedirs(REPORT_DIR, exist_ok=True)

# Load customer RFM report
rfm = pd.read_csv(
    os.path.join(REPORT_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Reports\\customer_rfm.csv")
)

# 1. Segment by city
city_segment = pd.crosstab(
    rfm["City"],
    rfm["Customer_Segment"]
)

# 2. Segment by age group
age_segment = pd.crosstab(
    rfm["Age_Band"],
    rfm["Customer_Segment"]
)

# 3. Segment by gender
gender_segment = pd.crosstab(
    rfm["Gender"],
    rfm["Customer_Segment"]
)

# 4. Segment by acquisition channel
channel_segment = pd.crosstab(
    rfm["Acquisition_Channel"],
    rfm["Customer_Segment"]
)

# 5. Churn analysis by segment
churn_segment = rfm.groupby(
    "Customer_Segment",
    observed=False
).agg(
    Total_Customers=("Customer_ID", "nunique"),
    Churned_Customers=("Churned", "sum")
).reset_index()

churn_segment["Churn_Rate_Percentage"] = (
    churn_segment["Churned_Customers"] /
    churn_segment["Total_Customers"]
) * 100

# Save reports
city_segment.to_csv(
    os.path.join(REPORT_DIR, "city_segment.csv")
)

age_segment.to_csv(
    os.path.join(REPORT_DIR, "age_segment.csv")
)

gender_segment.to_csv(
    os.path.join(REPORT_DIR, "gender_segment.csv")
)

channel_segment.to_csv(
    os.path.join(REPORT_DIR, "channel_segment.csv")
)

churn_segment.to_csv(
    os.path.join(REPORT_DIR, "churn_segment.csv"),
    index=False
)

# Display results
print("\nCUSTOMER SEGMENTS BY CITY")
print(city_segment)

print("\nCUSTOMER SEGMENTS BY AGE")
print(age_segment)

print("\nCUSTOMER SEGMENTS BY GENDER")
print(gender_segment)

print("\nCUSTOMER SEGMENTS BY ACQUISITION CHANNEL")
print(channel_segment)

print("\nCHURN ANALYSIS BY SEGMENT")
print(churn_segment)

print("\nAll reports saved successfully!")
