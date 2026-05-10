import pandas as pd
import matplotlib.pyplot as plt
from db_connection import conn

query = """
    with metrics as (
        select 
                p.category,
                oi.item_status,
                oi.quantity,
                oi.price_at_purchase,
                oi.quantity * oi.price_at_purchase as line_revenue
        from order_items oi
        join products p
            on oi.product_id = p.product_id
        where oi.item_status in ('Completed','Returned')
    ),
    category_revenue as (
        select 
                category,
                sum(line_revenue) as gross_revenue,
                sum(case
                        when item_status = 'Completed'
                        then line_revenue
                        else 0
                    end) as net_revenue,
                sum(case
                        when item_status = 'Returned'
                        then line_revenue
                        else 0
                    end) as return_loss
        from metrics
        group by category
    )
    select
            category,
            gross_revenue,
            net_revenue,
            return_loss,
            round(return_loss * 100.0 / nullif(gross_revenue,0),2) as return_loss_pct
    from category_revenue
    order by gross_revenue desc;
    """

df = pd.read_sql(query, conn)
print(df.head())

# SAVE TO CSV
df.to_csv('C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/csv/return_analysis.csv',
          index=False)

print("CSV saved successfully!")

print("Chart generation started...")

# VISUALIZATION
plt.figure(figsize=(10, 5))
plt.bar(df['category'], df['return_loss_pct'], color='salmon')
plt.title('Return Loss Percentage by Category')
plt.xlabel('Category') 
plt.ylabel('Return Loss')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig( 'C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/charts/return_loss_chart.png')

print("Return analysis completed and chart saved.")