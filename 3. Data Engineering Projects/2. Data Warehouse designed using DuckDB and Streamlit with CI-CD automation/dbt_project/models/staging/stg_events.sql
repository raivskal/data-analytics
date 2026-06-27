with source as (
    select * from {{ source('raw', 'raw_events') }}
),

renamed as (
    select
        event_id,
        customer_id,
        event_type,
        cast(event_timestamp as timestamp) as event_timestamp,
        device
    from source
)

select * from renamed
