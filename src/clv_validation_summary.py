import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BASE_DIR, "Reports")

results = pd.read_csv(
    os.path.join(REPORT_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Reports\\clv_validation_results.csv")
)

summary = {
    "Total Customers": len(results),
    "Average Historical Revenue": results["Historical_Revenue"].mean(),
    "Average Actual Future Revenue": results["Actual_Future_Revenue"].mean(),
    "Average Predicted Future Revenue": results["Predicted_Future_Revenue"].mean(),
    "Customers With Future Purchases": (
        results["Actual_Future_Revenue"] > 0
    ).sum(),
    "Customers Without Future Purchases": (
        results["Actual_Future_Revenue"] == 0
    ).sum()
}

summary_df = pd.DataFrame(
    list(summary.items()),
    columns=["Metric", "Value"]
)

summary_df.to_csv(
    os.path.join(REPORT_DIR, "clv_validation_summary.csv"),
    index=False
)

print("\n========== CLV VALIDATION SUMMARY ==========")
print(summary_df.to_string(index=False))

print("\nReport saved successfully!")