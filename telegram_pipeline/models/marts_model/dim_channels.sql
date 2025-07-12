-- models/marts/dimensions/dim_channels.sql

with unioned as (
    select distinct channel_name from {{ ref('stg_CheMed123') }}
    union
    select distinct channel_name from {{ ref('stg_tikvahpharma') }}
    union
    select distinct channel_name from {{ ref('stg_lobelia4cosmetics') }}
    union
    select distinct channel_name from {{ ref('stg_ethiopianfoodanddrugauthority') }}
),

final as (
    select
        row_number() over (order by channel_name) as channel_id,
        channel_name
    from unioned
)

select * from final
