with source as (
    select * from {{ source('raw', 'raw_customers') }}
),

renamed as (
    select
        customer_id,
        first_name,
        last_name,
        email,
        country,
        cast(created_at as timestamp) as created_at
    from source
)

select * from renamed
