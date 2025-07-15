from dagster import Definitions, ScheduleDefinition
from .jobs import medical_pipeline_job

# Define the daily schedule
daily_schedule = ScheduleDefinition(
    job=medical_pipeline_job,
    cron_schedule="0 8 * * *",  # Every day at 8 AM
    name="daily_medical_pipeline",
)

# Register job and schedule in the Dagster repository
defs = Definitions(
    jobs=[medical_pipeline_job],
    schedules=[daily_schedule],
)

