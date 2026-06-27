with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

events as (
    select * from {{ ref('stg_events') }}
),

customer_orders as (
    select
        customer_id,
        min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        count(order_id) as number_of_orders,
        sum(case when status = 'completed' then amount else 0 end) as total_spend
    from orders
    group by 1
),

customer_events as (
    select
        customer_id,
        count(event_id) as total_events,
        sum(case when event_type = 'page_view' then 1 else 0 end) as total_page_views
    from events
    group by 1
),

final as (
    select
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        c.country,
        c.created_at,
        coalesce(co.first_order_date, null) as first_order_date,
        coalesce(co.most_recent_order_date, null) as most_recent_order_date,
        coalesce(co.number_of_orders, 0) as number_of_orders,
        coalesce(co.total_spend, 0.0) as total_spend,
        coalesce(ce.total_events, 0) as total_events,
        coalesce(ce.total_page_views, 0) as total_page_views
    from customers as c
    left join customer_orders as co on c.customer_id = co.customer_id
    left join customer_events as ce on c.customer_id = ce.customer_id
)

select * from final
