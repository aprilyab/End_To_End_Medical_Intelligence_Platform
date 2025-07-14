with base as (
    select
        message_id,  -- remains text
        detected_object_class,
        confidence_score,
        image_path,
        detected_at
    from {{ source('raw', 'yolo_detections') }}
),

final as (
    select
        f.message_id,
        f.detected_object_class,
        f.confidence_score,
        f.image_path,
        f.detected_at
    from base f
    join {{ ref('fct_messages') }} m
      on f.message_id = m.telegram_message_id::text
)

select * from final

