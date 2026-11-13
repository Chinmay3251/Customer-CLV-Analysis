
import pandas as pd
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BASE_DIR, "Reports")

# Load RFM dataset
rfm = pd.read_csv(
    os.path.join(REPORT_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Reports\\customer_rfm.csv")
)

# Select features
X = rfm[["Recency", "Monetary"]].copy()

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train final K-Means model
kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

rfm["Cluster"] = kmeans.fit_predict(X_scaled)

# Calculate silhouette score
score = silhouette_score(
    X_scaled,
    rfm["Cluster"]
)

# Cluster summary
cluster_summary = rfm.groupby("Cluster").agg(
    Customer_Count=("Customer_ID", "nunique"),
    Average_Recency=("Recency", "mean"),
    Average_Monetary=("Monetary", "mean"),
    Total_Revenue=("Monetary", "sum"),
    Average_Frequency=("Frequency", "mean")
).reset_index()

# Revenue percentage
cluster_summary["Revenue_Percentage"] = (
    cluster_summary["Total_Revenue"] /
    cluster_summary["Total_Revenue"].sum()
) * 100

# Save outputs
rfm.to_csv(
    os.path.join(REPORT_DIR, "kmeans_customer_segments.csv"),
    index=False
)

cluster_summary.to_csv(
    os.path.join(REPORT_DIR, "kmeans_cluster_summary.csv"),
    index=False
)


# Assign business-friendly names
segment_names = {
    0: "At-Risk Customers",
    1: "Regular Customers",
    2: "High-Value Customers"
}

rfm["Business_Segment"] = rfm["Cluster"].map(segment_names)

cluster_summary["Business_Segment"] = (
    cluster_summary["Cluster"].map(segment_names)
)

# Add recommended strategies
strategies = {
    "At-Risk Customers":
        "Re-engagement campaigns and win-back offers",

    "Regular Customers":
        "Product recommendations and loyalty rewards",

    "High-Value Customers":
        "Premium offers and exclusive benefits"
}

cluster_summary["Recommended_Strategy"] = (
    cluster_summary["Business_Segment"].map(strategies)
)

# Save updated reports
rfm.to_csv(
    os.path.join(REPORT_DIR, "kmeans_customer_segments.csv"),
    index=False
)

cluster_summary.to_csv(
    os.path.join(REPORT_DIR, "kmeans_cluster_summary.csv"),
    index=False
)

print("\n========== BUSINESS SEGMENT STRATEGY ==========")
print(
    cluster_summary[
        ["Business_Segment", "Customer_Count",
         "Revenue_Percentage", "Recommended_Strategy"]
    ].to_string(index=False)
)

print("\nBusiness segment reports saved successfully!")


print("\n========== FINAL K-MEANS RESULTS ==========")
print("Number of clusters:", 3)
print(f"Silhouette Score: {score:.4f}")

print("\n========== CLUSTER SUMMARY ==========")
print(cluster_summary.to_string(index=False))

print("\nReports saved successfully!")
