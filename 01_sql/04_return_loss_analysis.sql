-- =====================================================
-- CATEGORY REVENUE & RETURN LOSS ANALYSIS
-- =====================================================

-- Business Question
-- Which categories generate revenue but lose heavily due to returns?

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