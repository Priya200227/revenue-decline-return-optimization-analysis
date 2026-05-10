import pandas as pd
import matplotlib.pyplot as plt
from db_connection import conn


query = """
SELECT
    customer_id,
    net_revenue

FROM vw_customer_summary

ORDER BY net_revenue DESC;
"""


df = pd.read_sql(query, conn)

print(df.head())


# CUMULATIVE REVENUE %
df['cumulative_revenue'] = df['net_revenue'].cumsum()

total_revenue = df['net_revenue'].sum()

df['cumulative_pct'] = (
    df['cumulative_revenue']
    / total_revenue
) * 100


# SAVE CSV
df.to_csv(
    'C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/csv/revenue_concentration.csv',
    index=False
)


# PARETO CHART
plt.figure(figsize=(12,6))

plt.plot(
    range(len(df)),
    df['cumulative_pct']
)

plt.axhline(
    y=80,
    linestyle='--'
)

plt.title('Revenue Concentration Pareto Analysis')

plt.xlabel('Customers Ranked by Revenue')

plt.ylabel('Cumulative Revenue %')


plt.savefig(
    'C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/charts/revenue_concentration_pareto.png'
)

print("Revenue concentration analysis completed!")