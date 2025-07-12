-- models/staging/stg_chemed123.sql
with raw_data as (

    select * from {{ source('raw', 'telegram') }}
    where channel = 'tikvahpharma'

),

cleaned as (

    select
        -- Core IDs
        id as telegram_message_id,
        json_id::text as original_message_id,

        -- Channel and metadata
        channel::text as channel_name,
        date::timestamp as message_timestamp,
        views::int as view_count,

        -- Main message content
        text::text as message_text,

        --  Derived fields
        length(text::text) as message_length, -- text length
        lower(split_part(text::text, ' ', 1)) as first_word, -- first word of message
        case
            when text ~ '[ሀ-ፐ]' then 'amharic'
            when text ~ '[a-zA-Z]' then 'english'
            else 'unknown'
        end as language_detected,

        --  Extract hashtag (if any)
        regexp_matches(text, '#\w+', 'g') as hashtags

    from raw_data

)

select * from cleaned

