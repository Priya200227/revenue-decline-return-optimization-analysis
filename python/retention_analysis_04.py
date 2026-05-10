import pandas as pd
from db_connection import conn


query = """
SELECT
    customer_id,
    completed_orders,
    net_revenue

FROM vw_customer_summary;
"""


df = pd.read_sql(query, conn)

print(df.head())


active_customers = df['customer_id'].count()

repeat_customers = df[
    df['completed_orders'] >= 2
]['customer_id'].count()

repeat_rate = round(
    (repeat_customers / active_customers) * 100,
    2
)


print("Active Customers:", active_customers)

print("Repeat Customers:", repeat_customers)

print("Repeat Rate %:", repeat_rate)


# SAVE CSV
df.to_csv(
    'C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/csv/retention_analysis.csv',
    index=False
)

print("Retention analysis completed!")