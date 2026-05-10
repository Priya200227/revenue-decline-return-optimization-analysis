-- =====================================================
-- MARGIN RISK MATRIX
-- =====================================================

-- Business Question
-- Which categories earn the most revenue but create the highest return-related margin risk?

with product_metrics as (
	select
			p.product_id,
            p.product_name,
            p.category,
            sum(case
					when oi.item_status = 'Completed'
                    then oi.quantity * oi.price_at_purchase
                    else 0 end) as net_revenue,
			sum(oi.quantity) as total_units,
             sum(case
					when oi.item_status = 'Returned'
                    then oi.quantity
                    else 0 end) as returned_units
	from products p
    join order_items oi
		on p.product_id = oi.product_id
	group by 
			p.product_id,
            p.product_name,
            p.category
),
category_summary as (
	select 
			category,
            sum(net_revenue) as category_revenue,
            sum(total_units) as total_units,
            sum(returned_units) as returned_units
	from product_metrics
    group by category
)
select
		category,
        round(category_revenue,0) as net_revenue,
        round(category_revenue * 100.0 /
			sum(category_revenue) over (),1) as revenue_share_pct,
		 round(returned_units * 100.0 /
			nullif(total_units,0),1) as return_rate_pct,
		case
			when ntile(4) over (order by category_revenue desc) = 1
					and ntile(4) over (order by 
											(returned_units * 1.0 / nullif(total_units,0))
										desc) = 1  
			then 'HIGH RISK - review immediately'
            when (
					returned_units * 1.0 / nullif(total_units,0)
				 ) > 0.15
			then 'MODERATE RISK - monitor'
            else 'LOW RISK'
		end as margin_risk_flag
from category_summary
order by category_revenue desc;