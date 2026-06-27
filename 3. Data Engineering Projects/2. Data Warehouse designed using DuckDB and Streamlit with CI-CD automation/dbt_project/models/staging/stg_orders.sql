with source as (
    select * from {{ source('raw', 'raw_orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        cast(order_date as timestamp) as order_date,
        status,
        cast(amount as decimal(10, 2)) as amount,
        payment_method
    from source
)

select * from renamed
