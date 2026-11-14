import os
import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(page_title="Customer CLV Analytics", page_icon="📊", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
REPORT_DIR = os.path.join(BASE_DIR, "Reports")


# LOAD DATA
@st.cache_data
def load_data():
    sales = pd.read_csv(os.path.join(DATA_DIR, "cleaned_sales.csv"))
    customers = pd.read_csv(os.path.join(DATA_DIR, "cleaned_customers.csv"))
    segments = pd.read_csv(os.path.join(REPORT_DIR, "kmeans_customer_segments.csv"))
    sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")
    return sales, customers, segments


try:
    sales, customers, segments = load_data()
except Exception as e:
    st.error(f"Unable to load project data: {e}")
    st.info("Check Data/cleaned_sales.csv, Data/cleaned_customers.csv, and Reports/kmeans_customer_segments.csv.")
    st.stop()


# PREPARE CUSTOMER SEGMENTS
required_columns = ["Customer_ID", "Business_Segment"]
missing_columns = [c for c in required_columns if c not in segments.columns]
if missing_columns:
    st.error("Missing columns in K-Means report: " + ", ".join(missing_columns))
    st.stop()

segment_mapping = segments[["Customer_ID", "Business_Segment"]].drop_duplicates("Customer_ID")

customer_data = customers.merge(segment_mapping, on="Customer_ID", how="left")
sales = sales.merge(segment_mapping, on="Customer_ID", how="left")

sales["Business_Segment"] = sales["Business_Segment"].fillna("Unclassified")
customer_data["Business_Segment"] = customer_data["Business_Segment"].fillna("Unclassified")


# DASHBOARD HEADER
st.title("📊 Customer CLV Analytics Dashboard")
st.caption("Retail Customer Segmentation, Revenue Analysis and Customer Value Insights")
st.divider()


# SIDEBAR FILTERS
st.sidebar.header("Dashboard Filters")

segment_options = sorted(sales["Business_Segment"].dropna().unique().tolist())
city_options = sorted(sales["City"].dropna().unique().tolist())
category_options = sorted(sales["Category"].dropna().unique().tolist())
channel_options = sorted(sales["Channel"].dropna().unique().tolist())


def reset_filters():
    st.session_state["selected_segments_filter"] = segment_options.copy()
    st.session_state["selected_cities_filter"] = city_options.copy()
    st.session_state["selected_categories_filter"] = category_options.copy()
    st.session_state["selected_channels_filter"] = channel_options.copy()


if "selected_segments_filter" not in st.session_state:
    st.session_state["selected_segments_filter"] = segment_options.copy()
if "selected_cities_filter" not in st.session_state:
    st.session_state["selected_cities_filter"] = city_options.copy()
if "selected_categories_filter" not in st.session_state:
    st.session_state["selected_categories_filter"] = category_options.copy()
if "selected_channels_filter" not in st.session_state:
    st.session_state["selected_channels_filter"] = channel_options.copy()

st.sidebar.button("Reset All Filters", on_click=reset_filters, use_container_width=True)

selected_segments = st.sidebar.multiselect(
    "Select Customer Segment", options=segment_options, key="selected_segments_filter"
)
selected_cities = st.sidebar.multiselect(
    "Select City", options=city_options, key="selected_cities_filter"
)
selected_categories = st.sidebar.multiselect(
    "Select Category", options=category_options, key="selected_categories_filter"
)
selected_channels = st.sidebar.multiselect(
    "Select Channel", options=channel_options, key="selected_channels_filter"
)


# APPLY FILTERS
filtered_sales = sales[
    sales["Business_Segment"].isin(selected_segments)
    & sales["City"].isin(selected_cities)
    & sales["Category"].isin(selected_categories)
    & sales["Channel"].isin(selected_channels)
].copy()

filtered_customers = customer_data[
    customer_data["Business_Segment"].isin(selected_segments)
].copy()
if "City" in filtered_customers.columns:
    filtered_customers = filtered_customers[
        filtered_customers["City"].isin(selected_cities)
    ]


# KPI CARDS
total_revenue = filtered_sales["Net_Revenue"].sum()
total_transactions = filtered_sales["Transaction_ID"].nunique()
total_customers = filtered_sales["Customer_ID"].nunique()
average_transaction_value = total_revenue / total_transactions if total_transactions > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Revenue", f"₹{total_revenue:,.2f}")
    st.caption("Revenue after returns and discounts")
with col2:
    st.metric("Total Customers", f"{total_customers:,}")
    st.caption("Unique customers in the dataset")
with col3:
    st.metric("Transactions", f"{total_transactions:,}")
    st.caption("Total recorded transactions")
with col4:
    st.metric("Average Transaction Value", f"₹{average_transaction_value:,.2f}")
    st.caption("Average revenue per transaction")

st.divider()


# 1. CUSTOMER SEGMENTATION
st.subheader("1. Customer Segmentation")

if not filtered_customers.empty:
    segment_summary = (
        filtered_customers.groupby("Business_Segment")
        .agg(Customers=("Customer_ID", "nunique"))
        .reset_index()
    )
    segment_revenue = (
        filtered_sales.groupby("Business_Segment")["Net_Revenue"]
        .sum()
        .reset_index()
    )
    segment_summary = segment_summary.merge(segment_revenue, on="Business_Segment", how="left")
    segment_summary["Net_Revenue"] = segment_summary["Net_Revenue"].fillna(0)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(
            segment_summary,
            names="Business_Segment",
            values="Customers",
            title="Customer Distribution by Segment",
            hole=0.4
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption(
             "Business Insight: Regular Customers form the largest group "
             "with 92 customers, followed by High-Value Customers with 62 "
             "and At-Risk Customers with 46. Focus on retaining valuable "
             "customers and improving engagement across all segments."
)

    with col2:
        fig = px.bar(
            segment_summary,
            x="Business_Segment",
            y="Net_Revenue",
            color="Business_Segment",
            title="Revenue by Customer Segment",
            text="Net_Revenue",
            labels={"Net_Revenue": "Revenue (₹)", "Business_Segment": "Segment"}
        )
        fig.update_traces(
            texttemplate="₹%{y:,.0f}",
            textposition="outside",
            cliponaxis=False
        )
        fig.update_layout(
            yaxis_title="Revenue (₹)",
            xaxis_title="Segment",
            uniformtext_minsize=8
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(
                    "Business Insight: High-Value Customers contribute the largest "
                    "share of revenue (43.53%), followed by Regular Customers (35.50%) "
                    "and At-Risk Customers (20.96%). Focus on retaining high-value "
                    "customers and re-engaging at-risk customers."
)

    st.dataframe(segment_summary, use_container_width=True, hide_index=True)
else:
    st.info("No customers found for the selected filters.")

st.divider()


# 2. REVENUE ANALYSIS
st.subheader("2. Revenue Analysis")

if not filtered_sales.empty:
    col1, col2 = st.columns(2)

    with col1:
        category_revenue = (
            filtered_sales.groupby("Category")["Net_Revenue"]
            .sum()
            .reset_index()
            .sort_values("Net_Revenue", ascending=False)
        )
        fig = px.bar(
            category_revenue,
            x="Category",
            y="Net_Revenue",
            title="Revenue by Product Category",
            color="Net_Revenue",
            text="Net_Revenue",
            labels={"Net_Revenue": "Revenue (₹)"}
        )
        fig.update_traces(texttemplate="₹%{y:,.0f}", textposition="outside", cliponaxis=False)
        fig.update_layout(uniformtext_minsize=8)
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption(
    "Business Insight: Apparel is the highest revenue-generating "
    "category, contributing ₹1,076,927, followed by Sports at "
    "₹1,013,288. Focus on maintaining strong-performing categories "
    "and identifying opportunities to improve lower-performing categories."
)

    with col2:
        city_revenue = (
            filtered_sales.groupby("City")["Net_Revenue"]
            .sum()
            .reset_index()
            .sort_values("Net_Revenue", ascending=False)
        )
        fig = px.bar(
            city_revenue,
            x="City",
            y="Net_Revenue",
            title="Revenue by City",
            color="Net_Revenue",
            text="Net_Revenue",
            labels={"Net_Revenue": "Revenue (₹)"}
        )
        fig.update_traces(texttemplate="₹%{y:,.0f}", textposition="outside", cliponaxis=False)
        fig.update_layout(uniformtext_minsize=8)
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption(
    "Business Insight: Chennai is the leading city by revenue, "
    "contributing approximately ₹1,023,296, followed by Pune "
    "at ₹1,000,715. Focus on understanding customer demand "
    "in high-performing cities and exploring growth opportunities "
    "in other locations."
)

    channel_revenue = filtered_sales.groupby("Channel")["Net_Revenue"].sum().reset_index()
    fig = px.pie(
        channel_revenue,
        names="Channel",
        values="Net_Revenue",
        title="Revenue Contribution by Sales Channel",
        hole=0.4
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption(
    "Business Insight: The chart shows how each sales channel "
    "contributes to total revenue. Use this comparison to identify "
    "strong-performing channels and opportunities to improve "
    "sales through other channels."
)
else:
    st.info("No revenue data is available for the selected filters.")

st.divider()


# 3. MONTHLY REVENUE TREND
st.subheader("3. Monthly Revenue Trend")

if not filtered_sales.empty:
    monthly_revenue = (
        filtered_sales.dropna(subset=["Date"])
        .assign(Month=lambda df: df["Date"].dt.to_period("M").astype(str))
        .groupby("Month")["Net_Revenue"]
        .sum()
        .reset_index()
    )
    fig = px.line(
        monthly_revenue,
        x="Month",
        y="Net_Revenue",
        markers=True,
        title="Monthly Revenue Trend",
        labels={"Net_Revenue": "Revenue (₹)"}
    )
    fig.update_traces(
        texttemplate="₹%{y:,.0f}",
        mode="lines+markers+text",
        textposition="top center"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    
    st.caption(
    "Business Insight: The monthly revenue trend helps identify "
    "changes in sales performance over time. Monitor revenue "
    "increases and decreases to identify seasonal patterns, "
    "evaluate business performance, and plan future sales strategies."
)
else:
    st.info("No monthly revenue data is available for the selected filters.")

st.divider()


# 4. SIX-MONTH REVENUE VALIDATION
st.subheader("4. Six-Month Revenue Validation")

validation_path = os.path.join(REPORT_DIR, "clv_validation_results.csv")

if os.path.exists(validation_path):
    validation = pd.read_csv(validation_path)
    validation = validation.merge(segment_mapping, on="Customer_ID", how="left")
    validation = validation[validation["Business_Segment"].isin(selected_segments)]

    if not validation.empty:
        mae = (
            validation["Actual_Future_Revenue"]
            - validation["Predicted_Future_Revenue"]
        ).abs().mean()

        rmse = (
            (
                validation["Actual_Future_Revenue"]
                - validation["Predicted_Future_Revenue"]
            ) ** 2
        ).mean() ** 0.5

        col1, col2 = st.columns(2)
        col1.metric("Six-Month Revenue MAE", f"₹{mae:,.2f}")
        col2.metric("Six-Month Revenue RMSE", f"₹{rmse:,.2f}")

        fig = px.scatter(
            validation,
            x="Actual_Future_Revenue",
            y="Predicted_Future_Revenue",
            color="Business_Segment",
            title="Actual vs Predicted Future Revenue",
            labels={
                "Actual_Future_Revenue": "Actual Revenue (₹)",
                "Predicted_Future_Revenue": "Predicted Revenue (₹)"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(
    "Business Insight: The six-month revenue validation compares "
    "actual revenue with predicted revenue. The improved baseline "
    "achieved an MAE of ₹8,934.36 and RMSE of ₹10,831.92, "
    "representing approximately 61.3% lower MAE than the initial "
    "naive baseline. This helps evaluate prediction accuracy."
)
    else:
        st.info("No validation records for the selected segments.")
else:
    st.warning("CLV validation report was not found.")

st.divider()


# 5. CUSTOMER DETAILS
st.subheader("5. Customer Details")

display_columns = [
    column for column in [
        "Customer_ID",
        "Business_Segment",
        "City",
        "Age_Band",
        "Gender",
        "Total_Orders",
        "Total_Revenue",
        "Churned"
    ]
    if column in filtered_customers.columns
]
st.dataframe(
    filtered_customers[display_columns],
    use_container_width=True,
    hide_index=True
)


# 6. BUSINESS RECOMMENDATIONS
st.divider()
st.subheader("6. Business Recommendations")
st.markdown("""
**High-Value Customers**
- Offer premium products and exclusive loyalty rewards.
- Focus on retention and personalized recommendations.

**Regular Customers**
- Recommend complementary products.
- Encourage larger purchases through product bundles.

**At-Risk Customers**
- Run win-back campaigns.
- Send personalized offers and purchase reminders.
""")


# 7. DOWNLOAD FILTERED REPORTS
st.divider()
st.subheader("7. Download Filtered Reports")

col1, col2 = st.columns(2)
with col1:
    customer_csv = filtered_customers.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Customer Data",
        data=customer_csv,
        file_name="filtered_customer_data.csv",
        mime="text/csv"
    )
with col2:
    sales_csv = filtered_sales.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Sales Data",
        data=sales_csv,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )


# 8. DYNAMIC BUSINESS INSIGHTS
st.divider()
st.subheader("8. Business Insights")

if not filtered_sales.empty:
    total_filtered_revenue = filtered_sales["Net_Revenue"].sum()
    top_category = filtered_sales.groupby("Category")["Net_Revenue"].sum().idxmax()
    top_city = filtered_sales.groupby("City")["Net_Revenue"].sum().idxmax()
    top_channel = filtered_sales.groupby("Channel")["Net_Revenue"].sum().idxmax()

    st.markdown(
        f"""
        - **Total filtered revenue:** ₹{total_filtered_revenue:,.2f}
        - **Top product category:** {top_category}
        - **Top revenue-generating city:** {top_city}
        - **Top sales channel:** {top_channel}
        """
    )

    if not filtered_customers.empty:
        segment_counts = (
            filtered_customers.groupby("Business_Segment")["Customer_ID"]
            .nunique()
        )
        largest_segment = segment_counts.idxmax()
        st.info(
            f"The largest selected customer segment is "
            f"**{largest_segment}**, with "
            f"**{segment_counts.max()} customers**."
        )
else:
    st.info("No business insights available for the selected filters.")


# FOOTER
st.caption("Customer CLV Analysis Project | Week 9 Dashboard")
