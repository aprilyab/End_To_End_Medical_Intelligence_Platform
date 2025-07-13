-- models/marts/facts/fct_messages.sql

with unioned as (
    select * from {{ ref('stg_CheMed123') }}
    union all
    select * from {{ ref('stg_tikvahpharma') }}
    union all
    select * from {{ ref('stg_lobelia4cosmetics') }}
    union all
    select * from {{ ref('stg_ethiopianfoodanddrugauthority') }}
),

messages as (
    select
        raw.*,
        c.channel_id,
        d.date_id
    from unioned raw
    left join {{ ref('dim_channels') }} c
        on raw.channel_name = c.channel_name
    left join {{ ref('dim_dates') }} d
        on raw.message_timestamp::date = d.date
)

select
    telegram_message_id,
    original_message_id,
    channel_id,
    date_id,
    message_timestamp,
    message_text,
    view_count,
    message_length,
    language_detected,
    array_length(hashtags, 1) as hashtag_count
from messages
