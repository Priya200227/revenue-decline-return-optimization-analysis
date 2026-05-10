import pandas as pd
import matplotlib.pyplot as plt
from db_connection import conn


query = """
WITH customer_rfm AS (

    SELECT
        o.customer_id,

        DATEDIFF(
            (SELECT MAX(order_date) FROM orders),
            MAX(o.order_date)
        ) AS recency_days,

        COUNT(DISTINCT o.order_id) AS frequency,

        SUM(
            oi.quantity * oi.price_at_purchase
        ) AS monetary_value

    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE oi.item_status = 'Completed'

    GROUP BY o.customer_id
),

rfm_scores AS (

    SELECT
        customer_id,
        recency_days,
        frequency,
        monetary_value,

        NTILE(5) OVER (
            ORDER BY recency_days ASC
        ) AS recency_score,

        NTILE(5) OVER (
            ORDER BY frequency DESC
        ) AS frequency_score,

        NTILE(5) OVER (
            ORDER BY monetary_value DESC
        ) AS monetary_score

    FROM customer_rfm
)

select 
		 customer_id,
        recency_days,
        frequency,
        monetary_value,
	    recency_score,
        frequency_score,
        monetary_score,
        case
			when recency_score >= 4
                 and frequency_score >= 4
                 and monetary_score >= 4
            then 'Champions'

            when frequency_score >= 4
                 and monetary_score >= 4
            then 'Loyal Customers'

            when recency_score <= 2
                 and frequency_score >= 3
            then 'At Risk'

            when recency_score <= 2
                 and frequency_score <= 2
            then 'Lost Customers'

            else 'Potential Loyalists'

        end as customer_segment

    from rfm_scores;
"""


df = pd.read_sql(query, conn)

print(df.head())


# SAVE CSV
df.to_csv(
    'C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/csv/churn_analysis.csv',
    index=False
)

# CUSTOMER SEGMENT DISTRIBUTION (RFM)
segment_counts = df['customer_segment'].value_counts()
plt.figure(figsize=(8, 6))
plt.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Customer RFM Segment Distribution')
plt.savefig(
    'C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/charts/customer_segment_distribution.png'
)

print("Churn analysis completed!")