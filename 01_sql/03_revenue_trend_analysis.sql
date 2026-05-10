-- =====================================================
-- REVENUE TREND ANALYSIS (MOM ANALYSIS)
-- =====================================================

create or replace view vw_customer_summary as
select
		o.customer_id,
        count(distinct o.order_id) as completed_orders,
        sum(oi.quantity * oi.price_at_purchase) as net_revenue
from orders o
join order_items oi
	on o.order_id = oi.order_id
where oi.item_status = 'Completed'
group by o.customer_id;


-- MONTH-OVER-MONTH REVENUE DECLINE ANALYSIS
-- Which months show revenue slowdown or decline?
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