#  End-to-End Medical Intelligence Platform

This project is an end-to-end data pipeline and reporting system that:

- Scrapes Telegram channels for medical-related posts.
- Stores the raw data in PostgreSQL.
- Transforms data using dbt.
- Runs object detection on images using YOLO.
- Exposes an API with FastAPI.
- Orchestrates the entire pipeline using Dagster.



##  Project Structure

End_To_End_Medical_Intelligence_Platform/
│
├── my_fastapi_app/ # FastAPI app exposing data APIs
│ ├── main.py # Entry point for FastAPI
│ ├── crud.py # DB logic
│ └── models.py # SQLAlchemy models
│
├── telegram_pipeline/ # dbt project for transformation
│ ├── models/
│ ├── dbt_project.yml
│ └── ...
│
├── medical_pipeline/ # Dagster orchestration project
│ ├── medical_pipeline/
│ │ ├── init.py
│ │ ├── ops.py # Dagster ops
│ │ ├── jobs.py # Dagster jobs
│ │ ├── repository.py # Dagster definitions
│ │ └── schedules.py # Dagster schedule
│ └── pyproject.toml
│
├── scrape_telegram.py # Script to scrape data from Telegram
├── load_raw_data.py # Script to load data to PostgreSQL
├── detect_objects_yolo.py # Script to run YOLO object detection
└── requirements.txt


---

##  How It Works

1. **Data is scraped** from medical Telegram channels.
2. **Raw data is loaded** into a PostgreSQL database.
3. **dbt models** clean and transform the raw data into dimensional models.
4. **YOLO model** detects objects in any attached media.
5. **FastAPI** provides endpoints to serve the transformed data.
6. **Dagster** orchestrates and schedules the pipeline.

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/medical-intelligence-platform.git
cd End_To_End_Medical_Intelligence_Platform
2. Create Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Requirements

    pip install -r requirements.txt
    Make sure requirements.txt includes:


    fastapi
    uvicorn
    sqlalchemy
    psycopg2
    dagster
    dagster-webserver
    dbt-core
    dbt-postgres
    pydantic
    opencv-python
    torch
    ultralytics
 Configuration
.env Example
Create a .env file in root:


DATABASE_URL=postgresql://user:password@localhost:5432/your_db
Make sure FastAPI and scripts read from this.

 Run FastAPI Server

cd my_fastapi_app
uvicorn main:app --reload
Access the API docs at: http://127.0.0.1:8000/docs

 Run dbt Transformations

cd telegram_pipeline
dbt run
 Run YOLO Object Detection

python detect_objects_yolo.py
 Orchestrate with Dagster
1. Run Dagster UI
cd medical_pipeline
dagster dev

Dagster UI: http://127.0.0.1:3000

 Schedule Pipeline
In medical_pipeline/medical_pipeline/schedules.py:

from dagster import ScheduleDefinition
from .jobs import medical_pipeline_job

daily_schedule = ScheduleDefinition(
    job=medical_pipeline_job,
    cron_schedule="0 8 * * *",  # Every day at 8 AM
    name="daily_medical_pipeline",
)
Schedules show up in Dagster UI under /schedules.

 API Endpoints
    Endpoint	Description
    /api/reports/top-products?limit=5	Top N messages/products
    /api/reports/top-hashtags?limit=10	Most used hashtags
    /api/reports/messages-by-date	Count of messages by day
    /api/reports/most-active-channels	Channels with most messages

See full docs at: http://127.0.0.1:8000/docs

 Testing
    Test DB connection with psql or any GUI client.

    Ensure YOLO outputs are visible in runs/detect/exp.

    Test endpoints using Swagger UI.

 Future Improvements
        Add unit tests with pytest.

        Dockerize pipeline for deployment.

        Integrate alerting for failed runs in Dagster.

        Upload YOLO detection results to cloud (e.g., S3).

👨‍⚕️ Authors
    Henok Yoseph

    Contributors welcome!

