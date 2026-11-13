
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BASE_DIR, "Reports")

# Load existing K-Means cluster summary
segments = pd.read_csv(
    os.path.join(REPORT_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Reports\\kmeans_cluster_summary.csv")
)

# Load baseline metrics
baseline = pd.read_csv(
    os.path.join(REPORT_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Reports\\baseline_metrics.csv")
)

# Get average transaction value
average_transaction_value = float(
    baseline.loc[
        baseline["Metric"] == "Average Transaction Value",
        "Value"
    ].iloc[0]
)

strategies = {
    "High-Value Customers": {
        "uplift_rate": 0.03,
        "strategy": "Premium offers and loyalty rewards"
    },
    "Regular Customers": {
        "uplift_rate": 0.05,
        "strategy": "Product bundles and cross-selling"
    },
    "At-Risk Customers": {
        "uplift_rate": 0.00,
        "strategy": "Win-back campaigns and reactivation"
    }
}

results = []

for _, row in segments.iterrows():

    segment_name = row["Business_Segment"]
    customers = int(row["Customer_Count"])
    historical_revenue = float(row["Total_Revenue"])

    assumptions = strategies[segment_name]

    if segment_name == "At-Risk Customers":

        # Assume 20% of at-risk customers return
        response_rate = 0.20

        expected_returning_customers = (
            customers * response_rate
        )

        additional_revenue = (
            expected_returning_customers
            * average_transaction_value
        )

    else:

        response_rate = assumptions["uplift_rate"]

        additional_revenue = (
            historical_revenue * response_rate
        )

    results.append({
        "Segment": segment_name,
        "Customers": customers,
        "Historical_Revenue": historical_revenue,
        "Assumed_Response_or_Uplift": response_rate * 100,
        "Estimated_Additional_Revenue": additional_revenue,
        "Strategy": assumptions["strategy"]
    })

impact = pd.DataFrame(results)

total_impact = impact["Estimated_Additional_Revenue"].sum()

impact.to_csv(
    os.path.join(REPORT_DIR, "upsell_business_impact.csv"),
    index=False
)

print("\n========== CUSTOMER STRATEGY ==========")
print(impact.to_string(index=False))

print("\n========== BUSINESS IMPACT ==========")
print("Estimated Additional Revenue: ₹",
      round(total_impact, 2))

print("\nReport saved successfully!")
