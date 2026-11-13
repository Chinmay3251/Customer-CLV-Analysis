
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="Customer CLV Analytics",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
REPORT_DIR = os.path.join(BASE_DIR, "Reports")


# ---------------------------------
# LOAD DATA
# ---------------------------------

@st.cache_data
def load_data():

    sales = pd.read_csv(
        os.path.join(DATA_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Data\\cleaned_sales.csv")
    )

    customers = pd.read_csv(
        os.path.join(DATA_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Data\\cleaned_customers.csv")
    )

    segments = pd.read_csv(
        os.path.join(REPORT_DIR, "C:\\Users\\MSI\\Desktop\\Internship\\Customer_CLV_Project\\Reports\\kmeans_customer_segments.csv")
    )

    sales["Date"] = pd.to_datetime(sales["Date"])

    return sales, customers, segments


try:
    sales, customers, segments = load_data()

except Exception as e:
    st.error(f"Unable to load project data: {e}")
    st.stop()


# ---------------------------------
# PREPARE CUSTOMER SEGMENTS
# ---------------------------------

if "Customer_ID" not in segments.columns:
    st.error("Customer_ID is missing from the K-Means report.")
    st.stop()

if "Business_Segment" not in segments.columns:
    st.error("Business_Segment is missing from the K-Means report.")
    st.stop()

segment_mapping = segments[
    ["Customer_ID", "Business_Segment"]
].drop_duplicates("Customer_ID")

customer_data = customers.merge(
    segment_mapping,
    on="Customer_ID",
    how="left"
)

sales = sales.merge(
    segment_mapping,
    on="Customer_ID",
    how="left"
)

sales["Business_Segment"] = (
    sales["Business_Segment"].fillna("Unclassified")
)

customer_data["Business_Segment"] = (
    customer_data["Business_Segment"].fillna("Unclassified")
)


# ---------------------------------
# DASHBOARD HEADER
# ---------------------------------

st.title("📊 Customer CLV Analytics Dashboard")

st.caption(
    "Retail Customer Segmentation, Revenue Analysis "
    "and Customer Value Insights"
)

st.divider()


# ---------------------------------
# SIDEBAR FILTERS
# ---------------------------------

st.sidebar.header("Dashboard Filters")

segment_options = sorted(
    sales["Business_Segment"].dropna().unique()
)

city_options = sorted(
    sales["City"].dropna().unique()
)

category_options = sorted(
    sales["Category"].dropna().unique()
)

channel_options = sorted(
    sales["Channel"].dropna().unique()
)

selected_segments = st.sidebar.multiselect(
    "Select Customer Segment",
    segment_options,
    default=segment_options
)

selected_cities = st.sidebar.multiselect(
    "Select City",
    city_options,
    default=city_options
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    category_options,
    default=category_options
)

selected_channels = st.sidebar.multiselect(
    "Select Channel",
    channel_options,
    default=channel_options
)


# ---------------------------------
# APPLY FILTERS
# ---------------------------------

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


# ---------------------------------
# KPI CARDS
# ---------------------------------

total_revenue = filtered_sales["Net_Revenue"].sum()

total_transactions = filtered_sales[
    "Transaction_ID"
].nunique()

total_customers = filtered_sales[
    "Customer_ID"
].nunique()

average_transaction_value = (
    total_revenue / total_transactions
    if total_transactions > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"₹{total_revenue:,.2f}"
)

col2.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col3.metric(
    "Transactions",
    f"{total_transactions:,}"
)

col4.metric(
    "Average Transaction Value",
    f"₹{average_transaction_value:,.2f}"
)

st.divider()


# ---------------------------------
# CUSTOMER SEGMENT ANALYSIS
# ---------------------------------

st.subheader("1. Customer Segmentation")

if not filtered_customers.empty:

    segment_summary = (
        filtered_customers.groupby("Business_Segment")
        .agg(
            Customers=("Customer_ID", "nunique")
        )
        .reset_index()
    )

    segment_revenue = (
        filtered_sales.groupby("Business_Segment")["Net_Revenue"]
        .sum()
        .reset_index()
    )

    segment_summary = segment_summary.merge(
        segment_revenue,
        on="Business_Segment",
        how="left"
    )

    segment_summary["Net_Revenue"] = (
        segment_summary["Net_Revenue"].fillna(0)
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            segment_summary,
            names="Business_Segment",
            values="Customers",
            title="Customer Distribution by Segment",
            hole=0.4
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            segment_summary,
            x="Business_Segment",
            y="Net_Revenue",
            color="Business_Segment",
            title="Revenue by Customer Segment",
            labels={
                "Net_Revenue": "Revenue (₹)",
                "Business_Segment": "Segment"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        segment_summary,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No customers found for the selected filters.")


st.divider()


# ---------------------------------
# REVENUE ANALYSIS
# ---------------------------------

st.subheader("2. Revenue Analysis")

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
        labels={"Net_Revenue": "Revenue (₹)"}
    )

    st.plotly_chart(fig, use_container_width=True)


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
        labels={"Net_Revenue": "Revenue (₹)"}
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------
# CHANNEL ANALYSIS
# ---------------------------------

channel_revenue = (
    filtered_sales.groupby("Channel")["Net_Revenue"]
    .sum()
    .reset_index()
)

fig = px.pie(
    channel_revenue,
    names="Channel",
    values="Net_Revenue",
    title="Revenue Contribution by Sales Channel",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)


st.divider()


# ---------------------------------
# MONTHLY REVENUE TREND
# ---------------------------------

st.subheader("3. Monthly Revenue Trend")

monthly_revenue = (
    filtered_sales.assign(
        Month=filtered_sales["Date"].dt.to_period("M").astype(str)
    )
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

st.plotly_chart(fig, use_container_width=True)


st.divider()


# ---------------------------------
# CLV VALIDATION
# ---------------------------------

st.subheader("4. Six-Month Revenue Validation")

validation_path = os.path.join(
    REPORT_DIR,
    "clv_validation_results.csv"
)

if os.path.exists(validation_path):

    validation = pd.read_csv(validation_path)

    validation = validation.merge(
        segment_mapping,
        on="Customer_ID",
        how="left"
    )

    validation = validation[
        validation["Business_Segment"].isin(selected_segments)
    ]

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
            "This is a six-month revenue run-rate baseline, "
            "not a full lifetime CLV prediction model."
        )

    else:
        st.info("No validation records for the selected segments.")

else:
    st.warning("CLV validation report was not found.")


st.divider()


# ---------------------------------
# CUSTOMER DETAILS
# ---------------------------------

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


# ---------------------------------
# BUSINESS RECOMMENDATIONS
# ---------------------------------

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

st.caption(
    "Customer CLV Analysis Project | Week 9 Dashboard v1"
)


# ---------------------------------
# 6. DOWNLOAD REPORTS
# ---------------------------------

st.divider()

st.subheader("6. Download Filtered Reports")

col1, col2 = st.columns(2)

with col1:
    customer_csv = filtered_customers.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Customer Data",
        data=customer_csv,
        file_name="filtered_customer_data.csv",
        mime="text/csv"
    )

with col2:
    sales_csv = filtered_sales.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Sales Data",
        data=sales_csv,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )


# ---------------------------------
# 7. DYNAMIC BUSINESS INSIGHTS
# ---------------------------------

st.divider()

st.subheader("7. Business Insights")

if not filtered_sales.empty:

    total_filtered_revenue = filtered_sales[
        "Net_Revenue"
    ].sum()

    top_category = (
        filtered_sales.groupby("Category")["Net_Revenue"]
        .sum()
        .idxmax()
    )

    top_city = (
        filtered_sales.groupby("City")["Net_Revenue"]
        .sum()
        .idxmax()
    )

    top_channel = (
        filtered_sales.groupby("Channel")["Net_Revenue"]
        .sum()
        .idxmax()
    )

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
            filtered_customers.groupby("Business_Segment")
            ["Customer_ID"].nunique()
        )

        largest_segment = segment_counts.idxmax()

        st.info(
            f"The largest selected customer segment is "
            f"**{largest_segment}**, with "
            f"**{segment_counts.max()} customers**."
        )

else:
    st.info("No business insights available for the selected filters.")
