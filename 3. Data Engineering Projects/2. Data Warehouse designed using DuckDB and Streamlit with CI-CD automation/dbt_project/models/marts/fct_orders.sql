with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

final as (
    select
        o.order_id,
        o.customer_id,
        o.order_date,
        o.status,
        o.amount,
        o.payment_method,
        c.country as customer_country,
        c.email as customer_email
    from orders as o
    left join customers as c on o.customer_id = c.customer_id
)

select * from final
