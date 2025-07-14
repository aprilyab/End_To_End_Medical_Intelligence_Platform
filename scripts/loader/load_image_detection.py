import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

#  Load credentials from .env
load_dotenv()

# PostgreSQL connection configuration
DB_NAME = "telegram_data"
DB_USER = "postgres"
DB_PASSWORD = "Henokpostgresql"
DB_HOST = "localhost"
DB_PORT = "5432"
SCHEMA_NAME = "raw"
TABLE_NAME = "yolo_detections"

CSV_FILE = "C:/Users/user/Desktop/tasks/End_To_End_Medical_Intelligence_Platform/data/raw/yolo_detections.csv"


#  Read CSV
df = pd.read_csv(CSV_FILE)

# Optional: Sanitize column names
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

#  Create table if not exists
columns = df.columns
column_defs = ",\n".join(f"{col} TEXT" for col in columns)

create_table_sql = f"""
CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.{TABLE_NAME} (
    id SERIAL PRIMARY KEY,
    {column_defs}
);
"""
cursor.execute(create_table_sql)

#  Insert data
for _, row in df.iterrows():
    insert_sql = sql.SQL("INSERT INTO {}.{} ({}) VALUES ({})").format(
        sql.Identifier(SCHEMA_NAME),
        sql.Identifier(TABLE_NAME),
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )
    cursor.execute(insert_sql, tuple(str(row[col]) for col in columns))

#  Finalize
conn.commit()
cursor.close()
conn.close()

print(f"✅ {len(df)} rows inserted into {SCHEMA_NAME}.{TABLE_NAME}")
