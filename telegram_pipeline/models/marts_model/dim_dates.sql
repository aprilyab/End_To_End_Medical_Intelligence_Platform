-- models/marts/dimensions/dim_dates.sql

with dates as (
    select generate_series(
        '2024-01-01'::date,
        '2025-12-31'::date,
        interval '1 day'
    )::date as date
),

final as (
    select
        row_number() over (order by date) as date_id,
        date,
        extract(year from date) as year,
        extract(month from date) as month,
        extract(day from date) as day,
        to_char(date, 'Day') as weekday,
        to_char(date, 'YYYY-MM') as year_month
    from dates
)

select * from final
