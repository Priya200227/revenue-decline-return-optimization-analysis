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


create or replace view vw_product_summary as
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