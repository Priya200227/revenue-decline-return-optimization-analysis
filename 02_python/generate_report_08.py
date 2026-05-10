import pandas as pd
import os

# Load analysis results from CSV files
revenue_df = pd.read_csv('C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/csv/revenue_analysis.csv')
return_df = pd.read_csv('C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/csv/return_analysis.csv')
retention_df = pd.read_csv('C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/csv/retention_analysis.csv')
churn_df = pd.read_csv('C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/csv/churn_analysis.csv')
revenue_concentration_df = pd.read_csv('C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/csv/revenue_concentration.csv')


# ==============================
# KPI EXTRACTION
# ==============================

latest_revenue = revenue_df['monthly_net_revenue'].iloc[-1]
previous_revenue = revenue_df['monthly_net_revenue'].iloc[-2]
mom_growth = revenue_df['mom_growth_pct'].iloc[-1]


# Return risk analysis
highest_return_row = return_df.sort_values(
        by='return_loss_pct', ascending=False).iloc[0]

highest_return_category = highest_return_row['category']

highest_return_pct = highest_return_row['return_loss_pct']


# Retention analysis
total_customers = len(retention_df)

repeat_customers = retention_df[
            retention_df['completed_orders'] >= 2].shape[0]

repeat_rate = round((repeat_customers / total_customers) * 100, 2)


# RFM analysis
top_segment = churn_df['customer_segment'].value_counts().idxmax()

top_segment_count = churn_df [churn_df['customer_segment'] == top_segment].shape[0]


# Revenue concentration analysis
top_20_index = int(len(revenue_concentration_df) * 0.2)

top_20_revenue_pct = revenue_concentration_df['cumulative_pct'].iloc[
    top_20_index]


# ==============================
# DYNAMIC BUSINESS INTERPRETATIONS

if mom_growth < 0:
    revenue_comment = (
        "Revenue declined compared to the previous month, "
        "indicating potential slowdown in business performance."
    )
else:
    revenue_comment = (
        "Revenue growth remained positive in the latest month, "
        "indicating continued business expansion."
    )


if highest_return_pct > 20:
    return_comment = (
        f"{highest_return_category} shows elevated return-related "
        "margin risk and requires immediate operational review."
    )
else:
    return_comment = (
        f"{highest_return_category} has moderate return risk "
        "compared to other categories."
    )


if repeat_rate < 40:
    retention_comment = (
        "Customer retention is relatively weak, suggesting "
        "possible customer satisfaction or loyalty challenges."
    )
else:
    retention_comment = (
        "Repeat customer contribution remains healthy, "
        "supporting recurring revenue stability."
    )


if top_20_revenue_pct > 80:
    concentration_comment = (
        "Revenue is highly concentrated among a small customer group, "
        "creating dependency risk."
    )
else:
    concentration_comment = (
        "Revenue concentration risk remains relatively balanced."
    )


# ==============================
# REPORT GENERATION 
# ==============================

report = f"""

============================================================
Revenue Decline & Return Optimization Analysis Report
============================================================


EXECUTIVE SUMMARY
------------------------------------------------------------

Latest Monthly Revenue:
{latest_revenue:,.2f}

Previous Monthly Revenue:
{previous_revenue:,.2f}

Month-over-Month Growth:
{mom_growth}%


{revenue_comment}


RETURN RISK ANALYSIS
------------------------------------------------------------

Highest Return Risk Category:
{highest_return_category}

Return Loss Percentage:
{highest_return_pct}%


{return_comment}


CUSTOMER RETENTION ANALYSIS
------------------------------------------------------------

Total Active Customers:
{total_customers}

Repeat Customers:
{repeat_customers}

Repeat Rate:
{repeat_rate}%


{retention_comment}


CUSTOMER CHURN & RFM ANALYSIS
------------------------------------------------------------

Largest Customer Segment:
{top_segment}

Customers in Segment:
{top_segment_count}


The RFM model identified customer lifecycle patterns
based on recency, frequency, and monetary contribution.


REVENUE CONCENTRATION ANALYSIS
------------------------------------------------------------

Top 20% Customer Revenue Contribution:
{round(top_20_revenue_pct,2)}%


{concentration_comment}


BUSINESS RECOMMENDATIONS
------------------------------------------------------------

1. Investigate high-return products within the
   {highest_return_category} category.

2. Strengthen quality checks and fulfillment processes
   to reduce return-related losses.

3. Improve retention strategies targeting repeat
   and high-value customers.

4. Monitor revenue concentration risk to reduce
   dependency on a limited customer base.

5. Continuously monitor MoM revenue trends for
   early detection of business slowdown.


============================================================
End of Report
============================================================

"""


# ============================================
# PRINT REPORT
# ============================================

print(report)


# ============================================
# CREATE REPORT DIRECTORY
# ============================================

os.makedirs(
    'C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/report',
    exist_ok=True
)


# ============================================
# SAVE REPORT
# ============================================

with open(
    'C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/report/business_report.txt',
    'w',
    encoding='utf-8'
) as file:

    file.write(report)


print("Business report generated successfully!")