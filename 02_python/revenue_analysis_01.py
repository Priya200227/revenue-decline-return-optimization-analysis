import pandas as pd
import matplotlib.pyplot as plt
from db_connection import conn
 
query = """
with monthly_revenue as (
	select 
			date_format(o.order_date, '%Y-%m') as monthly,
            sum(case 
					when oi.item_status = 'Completed'
                    then oi.quantity * oi.price_at_purchase
                    else 0
                    end) as monthly_net_revenue,
			count(distinct case
								when oi.item_status = 'Completed' 
                                then o.order_id
                                else 0
                                end) as monthly_orders
from orders o
join order_items oi
	on o.order_id = oi.order_id
group by monthly
),
monthly_growth as (
	select monthly,
		   monthly_net_revenue,
           monthly_orders,
           lag(monthly_net_revenue) over(order by monthly) as previous_month_revenue,
		   sum(monthly_net_revenue) over() as cummulative_revenue
	from monthly_revenue
)
select 
		monthly,
        monthly_net_revenue,
        monthly_orders,
        (monthly_net_revenue - previous_month_revenue) as mom_revenue_change,
        round((monthly_net_revenue - previous_month_revenue) * 100.0 / 
        nullif(previous_month_revenue,0),2) as mom_growth_pct,
        cummulative_revenue
from monthly_growth
order by monthly;
"""

df = pd.read_sql(query,conn)
print(df.head())

# SAVE CSV
df.to_csv(
    'C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/csv/revenue_analysis.csv',
    index= False
 )

# CREATE CHART
plt.figure(figsize=(10,5))

plt.plot(
    df['monthly'], df['monthly_net_revenue']   
)

plt.xticks(rotation=45)
plt.title('Monthly Net Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Net Revenue')
plt.savefig('C:/Users/priya/OneDrive/Desktop/DataAnalytics2026/01_Revenue-Decline-Return-Optimization-Analysis/04_outputs/charts/revenue_trend.png')
print("Revenue trend chart saved successfully!")
