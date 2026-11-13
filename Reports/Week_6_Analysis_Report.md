# Week 6 – Customer Segmentation and CLV Analysis Report

## 1. Project Overview

**Project:** Customer Lifetime Value (CLV) Analysis  
**Project Type:** Retail Customer Segmentation and Revenue Analysis  
**Tools:** Python, Pandas, NumPy, Scikit-learn, Matplotlib, Git and Power BI (planned)

### Objective

The objective of this project is to understand customer purchasing behaviour, identify valuable customer groups, estimate future customer revenue and develop targeted upselling and retention strategies.

**Scope clarification:** The original project brief described an insurance comparison portal. However, the two available datasets contain retail sales transactions and customer profiles. Therefore, the analysis has been adapted to retail customer segmentation and customer value analysis.

## 2. Dataset Overview

Two datasets were used:

1. `da_sales_transactions.csv`
   - 1,000 transaction records
   - 11 columns
   - Includes customer IDs, transaction dates, products, categories, units, prices, discounts, channels, cities and returns.

2. `da_customer_profiles.csv`
   - 200 customer records
   - 10 columns
   - Includes customer demographics, acquisition channels, purchase dates, total orders, revenue and churn status.

### Data Quality Findings

- No missing values were identified.
- No duplicate transaction IDs or customer IDs were identified.
- All 200 customers in the profile dataset matched customers in the sales dataset.
- 42 customer records had a first purchase date later than their last purchase date.
- Original data was preserved, and the date inconsistencies were documented.

## 3. Baseline Business Metrics

| Metric | Result |
|---|---:|
| Total Transactions | 1,000 |
| Total Customers | 200 |
| Gross Revenue | ₹84,56,050 |
| Revenue After Discounts | ₹80,21,851.20 |
| Realized Revenue After Returns | ₹72,00,464.20 |
| Returned Transactions | 97 |
| Return Rate | 9.7% |
| Average Transaction Value | ₹7,200.46 |
| Active Customers | 194 |
| Churned Customers | 6 |
| Churn Rate | 3% |
| Average Revenue Per Customer | ₹36,002.32 |

The average transaction value is calculated using the available transaction records. It should not automatically be interpreted as an order-level average.

## 4. RFM Analysis

RFM analysis was conducted using:

- Recency: Days since the customer's most recent transaction.
- Frequency: Number of unique transactions.
- Monetary: Total realized revenue.

The analysis date was 29 June 2026, one day after the last transaction date.

### RFM Segment Results

| Segment | Customers | Revenue Contribution |
|---|---:|---:|
| Low Value | 40 | 14.02% |
| Below Average | 40 | 16.92% |
| Average | 40 | 18.56% |
| High Value | 40 | 22.90% |
| Top Value | 40 | 27.59% |

High-value and top-value customers together contributed approximately 50.49% of revenue.

**Observation:** All customers had five unique transactions. Therefore, Frequency did not distinguish customers, and the frequency score was assigned a neutral value of 3. These five RFM groups are exploratory equal-sized quintiles, not naturally discovered clusters.

## 5. Customer Behaviour Analysis

The analysis examined revenue by product category, city and sales channel.

### Key Findings

- Apparel generated the highest category revenue: ₹10,76,926.80.
- Chennai generated the highest city revenue: ₹10,23,296.30.
- Website generated the highest channel revenue: ₹19,07,778.65.

Customer profiles were also examined by age, gender, city and acquisition channel.

Only six customers were marked as churned in the customer profile dataset. Consequently, churn-related findings should be interpreted cautiously.

## 6. K-Means Customer Segmentation

K-Means clustering was performed using:

- Recency
- Monetary value

Frequency was excluded because all customers had the same transaction count.

StandardScaler was used to scale the features before clustering.

### Model Selection

The silhouette scores were compared across different values of K.

| K | Silhouette Score |
|---|---:|
| 2 | 0.3951 |
| 3 | 0.4175 |
| 4 | 0.3801 |
| 5 | 0.3706 |
| 6 | 0.3751 |
| 7 | 0.3915 |

K=3 produced the highest silhouette score.

**Final silhouette score: 0.4175**

The model identified three customer segments.

### Final Customer Segments

| Segment | Customers | Revenue Contribution |
|---|---:|---:|
| At-Risk Customers | 46 | 20.96% |
| Regular Customers | 92 | 35.50% |
| High-Value Customers | 62 | 43.53% |

### Business Interpretation

**At-Risk Customers:** These customers had the highest average recency, approximately 315 days. Win-back campaigns may help encourage repeat purchases.

**Regular Customers:** These customers represented the largest segment, with 92 customers. Cross-selling, product bundles and loyalty rewards may increase their spending.

**High-Value Customers:** These customers generated approximately 43.53% of total revenue. Premium recommendations and exclusive loyalty benefits may help retain them.

The segment labels are business interpretations of the cluster characteristics, not confirmed churn classifications.

## 7. Customer Value and Revenue Forecast Validation

A historical customer revenue baseline was calculated using realized transaction revenue.

A time-based validation approach was used:

- Historical period: Before 28 December 2025.
- Validation period: 28 December 2025 to 28 June 2026.
- Total customers evaluated: 200.
- Customers with future-period purchases: 141.
- Customers without future-period purchases: 59.

A simple revenue run-rate baseline was used to estimate equivalent six-month revenue.

### Validation Results

| Metric | Result |
|---|---:|
| Average Historical Revenue | ₹28,267.76 |
| Average Actual Future Revenue | ₹7,734.56 |
| Average Predicted Future Revenue | ₹9,483.21 |
| MAE | ₹8,934.36 |
| RMSE | ₹10,831.92 |

The improved run-rate baseline reduced MAE by approximately 61.3% compared with the original naïve baseline.

**Limitation:** This is a six-month revenue forecasting baseline, not a fully developed predictive customer lifetime value model. The available datasets do not provide profit margins, acquisition costs, discount rates or customer lifetime assumptions. The original target of CLV MAE below ₹500 has not been achieved.

## 8. Three-Tier Upsell and Retention Strategy

### Tier 1: High-Value Customers

**Customers:** 62

**Strategy:**
- Premium product recommendations.
- Exclusive loyalty rewards.
- Early access to new products.
- Personalized offers.

**Scenario assumption:** 3% additional revenue uplift.

**Estimated additional revenue:** ₹94,039.91.

### Tier 2: Regular Customers

**Customers:** 92

**Strategy:**
- Product bundles.
- Cross-selling complementary products.
- Larger-purchase incentives.
- Loyalty points.

**Scenario assumption:** 5% additional revenue uplift.

**Estimated additional revenue:** ₹1,27,818.65.

### Tier 3: At-Risk Customers

**Customers:** 46

**Strategy:**
- Personalized win-back campaigns.
- Limited-time offers.
- Purchase reminders.
- Recommendations based on previous purchases.

**Scenario assumption:** 20% of customers return and make one average-value purchase.

**Estimated additional revenue:** ₹66,244.23.

## 9. Estimated Business Impact

| Segment | Estimated Additional Revenue |
|---|---:|
| High-Value Customers | ₹94,039.91 |
| Regular Customers | ₹1,27,818.65 |
| At-Risk Customers | ₹66,244.23 |
| **Total** | **₹2,88,102.78** |

The estimated additional revenue is a scenario based on assumed response and uplift rates. It is not guaranteed revenue or a result of a completed marketing campaign.

The estimate is based on revenue, not profit, and does not deduct campaign costs or discounts.

## 10. Limitations

1. Only 200 customer profiles and 1,000 transactions were available.
2. The original insurance project scope could not be implemented because the available data was retail-based.
3. All customers had the same transaction frequency.
4. The K-Means silhouette score was 0.4175, below the original target of 0.85.
5. Only six customers were marked as churned.
6. The CLV validation model is a simple revenue run-rate baseline.
7. The business impact estimates depend on assumed uplift and response rates.
8. The 42 inconsistent customer purchase-date sequences require further investigation.

## 11. Conclusion

The analysis identified three useful customer groups using K-Means clustering and revealed differences in customer value and purchasing behaviour.

High-value customers contributed the largest share of revenue, while regular customers represented the largest customer group. At-risk customers offer a potential opportunity for re-engagement.

The proposed three-tier strategy estimates an additional revenue opportunity of ₹2,88,102.78 under the stated assumptions.

Further work should focus on improving predictive revenue modelling, validating marketing assumptions and developing an interactive Streamlit dashboard.

**Overall Status:** Week 6 analytical work completed, subject to documentation review and Git submission.