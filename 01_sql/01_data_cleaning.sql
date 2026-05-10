-- CHECK NULLS
select * from orders 
where order_id is null;

select * from orders_items
where product_id is null;

select * from customers
where customer_id is null;

-- CHECK DUPLICATES
select order_id, count(*) from orders
group by order_id
having count(*) >1;

-- STANDARDIZE ITEM STATUS
select distinct item_status
from order_items;
