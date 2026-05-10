-- =====================================================
-- REVENUE CONCENTRATION & DEPENDENCY ANALYSIS
-- =====================================================

-- Business Question:
-- Is business revenue heavily dependent on a small group of customers?

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

-- CUSTOMER REVENUE DISTRIBUTION
select
		customer_id,
        net_revenue,
        sum(net_revenue) over () as total_revenue,
        row_number() over (order by net_revenue desc) as revenue_rank,
        sum(net_revenue) over (order by net_revenue desc) as cumulative_revenue,
        round(sum(net_revenue) over (order by net_revenue desc) * 100.0 /
				sum(net_revenue) over (),2) as cumulative_revenue_pct
from vw_customer_summary;
                
  
  -- TOP 20% CUSTOMER REVENUE CONTRIBUTION
  with ranked_customers as (
	select
			customer_id,
            net_revenue,
            ntile(5) over (order by net_revenue desc) as customer_bucket
	from vw_customer_summary
  )
select
		sum(net_revenue) as total_revenue,
        sum(case
				when customer_bucket = 1
                then net_revenue
                else 0 end) as revenue_top_20_customers,
		 round(sum(case
				when customer_bucket = 1
                then net_revenue
                else 0 end) * 100.0 / sum(net_revenue),2) as revenue_contribution_pct
from ranked_customers;