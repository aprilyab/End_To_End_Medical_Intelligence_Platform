from dagster import op
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(["python", "scrape_telegram.py"], check=True)

@op
def load_raw_to_postgres():
    subprocess.run(["python", "load_raw_data.py"], check=True)

@op
def run_dbt_transformations():
    subprocess.run(["dbt", "run", "--project-dir", "telegram_pipeline"], check=True)

@op
def run_yolo_enrichment():
    subprocess.run(["python", "detect_objects_yolo.py"], check=True)
