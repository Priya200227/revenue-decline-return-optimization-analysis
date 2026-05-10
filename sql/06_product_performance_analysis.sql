-- =====================================================
-- HIGH RETURN PRODUCTS
-- =====================================================
-- Business Question
-- Which products are driving excessive returns and profitability leakage?
with product_metrics as (
	select 	
			p.product_id,
            p.product_name,
            p.category,
            sum(case
					when oi.item_status = 'Completed'
                    then oi.quantity
                    
                    else 0
				end
				) as units_sold,
			 sum(case
					when oi.item_status = 'Completed'
                    then oi.quantity * oi.price_at_purchase
                    else 0
				end
				) as net_revenue,
			 sum(oi.quantity) as total_units,
             sum(case
					when oi.item_status = 'Returned'
                    then oi.quantity
                    else 0
				end
				) as returned_units
	from products p
    join order_items oi
		on p.product_id = oi.product_id
    group by p.product_id,
             p.product_name,
             p.category
)
select product_name,
	   category,
       units_sold,
       net_revenue,
       returned_units,
       round(returned_units * 100.0 / nullif(total_units,0),2) as return_rate_pct
from product_metrics
order by return_rate_pct desc
limit 10;


-- =====================================================
-- PRODUCT PERFORMANCE ANALYSIS
-- =====================================================
-- Business Question
-- Which products are driving revenue, demand, and return-related losses?

create or replace view vw_product_metrics as
select
		p.product_id, 
        p.product_name, 
        p.category,
        sum(case 
				when oi.item_status = 'Completed' 
                then oi.quantity 
                else 0 
                end) as units_sold,
         sum(case
				when oi.item_status = 'Completed'
                then oi.quantity * oi.price_at_purchase
                else 0
                end) as net_revenue,
		 sum(case
				when oi.item_status = 'Completed'
                then oi.quantity
                else 0
                end) as returned_units
from products p
join order_items oi
	on p.product_id = oi.product_id
group by p.product_id, p.product_name, p.category;

-- TOP PRODUCTS BY REVENUE
select
		product_name,
        category,
        units_sold,
        net_revenue,
        rank() over (order by net_revenue desc) as revenue_rank
from vw_product_metrics
order by revenue_rank
limit 10;


-- TOP PRODUCTS BY DEMAND
select
		product_name,
        category,
        units_sold,
        net_revenue,
        rank() over (order by units_sold desc) as demand_rank
from vw_product_metrics
order by demand_rank
limit 10;


-- HIGH RETURN PRODUCTS
select
		product_name,
        category,
        units_sold,
        net_revenue,
        returned_units,
        round(returned_units * 100.0 / nullif(total_units,0),2) as return_rate_pct
from vw_product_metrics
order by return_rate_pct desc
limit 10;


-- PRODUCT_REVENUE_CONTRIBUTION
select
		product_name,
        category,
        net_revenue,
        round(net_revenue * 100.0 / sum(net_revenue) over (),2) as revenue_contribution_pct,
        rank() over (order by net_revenue desc) as revenue_rank
from vw_product_metrics
order by revenue_rank;


-- CATEGORY PRODUCT PERFORMANCE
select
		category,
        count(product_id) as total_products,
        sum(units_sold) as units_sold,
        sum(net_revenue) as revenue
from vw_product_metrics
group by category
order by revenue desc;


-- LOW-PERFORMING PRODUCTS
-- Threshold: products with fewer than 10 completed units sold
select
		product_name,
        category,
        units_sold,
        net_revenue
from vw_product_metrics
where units_sold < 10
order by net_revenue;