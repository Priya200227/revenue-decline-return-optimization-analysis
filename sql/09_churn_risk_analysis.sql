-- =====================================================
-- CUSTOMER CHURN RISK ANALYSIS (RFM)
-- =====================================================

-- Business Question:
-- Which customers are most at risk of churn
-- and which customer groups generate the most value?

with customer_rfm as (
	select 
			o.customer_id,
            
            -- RECENCY
            datediff(
				(select max(order_date) from orders),
                max(o.order_date)
            ) as recency_days,
            
            -- FREQUENCY
            count(distinct o.order_id) as frequency,
            
            -- MONETARY
            sum(oi.quantity * oi.price_at_purchase) as monetary_value
            
	from orders o
    join order_items oi
		on o.order_id = oi.order_id
	where oi.item_status = 'Completed'
    group by o.customer_id
),
rfm_scores as (
	select
			customer_id,
            recency_days,
            frequency,
            monetory_value,
            -- Higher score = better customer
            -- Lower recency_days is better
            ntile(5) over (order by recency_days asc) as recency_score,
            -- Higher frequency is better
            ntile(5) over (order by frequency asc) as frequency_score,
             -- Higher monetary value is better
            ntile(5) over (order by monetary_value asc) as monetary_score
    from customer_rfm
),
rfm_segments as (
select
		customer_id,
        recency_days,
        frequency,
        monetary_value,
	    recency_score,
        frequency_score,
        monetary_score,
        case
			-- Best customers
			when recency_score >= 4
                 and frequency_score >= 4
                 and monetary_score >= 4
            then 'Champions'
            
			-- Frequent high spenders
            when frequency_score >= 4
                 and monetary_score >= 4
            then 'Loyal Customers'

			-- Previously active but becoming inactive
            when recency_score <= 2
                 and frequency_score >= 3
            then 'At Risk'

			-- Low engagement customers
            when recency_score <= 2
                 and frequency_score <= 2
            then 'Lost Customers'

			-- Moderate customers with growth potential
            else 'Potential Loyalists'

        end as customer_segment

    from rfm_scores
)
select
    customer_segment,
	count(*) as customers,
	round(
        avg(recency_days),0) as avg_recency_days,
	round(
        avg(frequency),1) as avg_frequency,
	round(
        avg(monetary_value),0) as avg_monetary_value,
	round(
        sum(monetary_value) * 100.0
        / sum(sum(monetary_value)) over (),2) as revenue_pct
from rfm_segments
group by customer_segment
order by revenue_pct desc;