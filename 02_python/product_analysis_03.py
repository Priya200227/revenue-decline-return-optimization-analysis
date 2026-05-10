import pandas as pd
import matplotlib.pyplot as plt
from db_connection import conn


query = """
SELECT
    product_name,
    category,
    units_sold,
    net_revenue,
    returned_units

FROM vw_product_metrics

ORDER BY net_revenue DESC
LIMIT 10;
"""


df = pd.read_sql(query, conn)

print(df.head())


# SAVE CSV
df.to_csv(
    'C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/csv/product_analysis.csv',
    index=False
)

# TOP PRODUCT REVENUE CHART
plt.figure(figsize=(10, 6))
plt.bar(df['product_name'], df['net_revenue'], color='skyblue')
plt.xlabel('Product')
plt.ylabel('Revenue')
plt.title('Top 10 Products by Revenue')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(
    'C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/charts/top_products_revenue.png'
)
print("Product analysis completed!")