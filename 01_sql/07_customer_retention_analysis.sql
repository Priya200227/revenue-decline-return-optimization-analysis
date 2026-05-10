-- =====================================================
-- CUSTOMER RETENTION ANALYSIS
-- =====================================================

-- Business Question:
-- Are customers returning and sustaning business revenue?

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

-- CUSTOMER RETENTION & LOYALITY STRENGTH
-- ACTIVE vs REPEAT CUSTOMERS
select
		count(customer_id) as active_customers,
        count(case
					when completed_orders >=2
                    then customer_id
				end) as repeat_customers,
		round(count(case
					when completed_orders >=2
                    then customer_id
				end) * 100.0 / nullif(count(customer_id),0),2) as repeat_rate_pct,
		round(avg(completed_orders),2) as avg_orders_per_customer,
        round(avg(net_revenue),2) as avg_revenue_per_customer
from vw_customer_summary;

-- LOYAL CUSTOMER REVENUE CONTRIBUTION
-- Customers with 5+ completed orders are treated as loyal customers
select
		sum(net_revenue) as total_revenue,
        sum(case
				when completed_orders >=5
                then net_revenue
                else 0 end) as loyal_customer_revenue,
		 round(sum(case
				when completed_orders >=5
                then net_revenue
                else 0 end) * 100 / sum(net_revenue),2) as loyal_customer_contribution_pct
from vw_customer_summary;