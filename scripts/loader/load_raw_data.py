import os
import json
import pandas as pd
import psycopg2
from psycopg2 import sql

# PostgreSQL connection configuration
DB_NAME = "telegram_data"
DB_USER = "postgres"
DB_PASSWORD = "Henokpostgresql"
DB_HOST = "localhost"
DB_PORT = "5432"
SCHEMA_NAME = "raw"
TABLE_NAME = "telegram"

# Path to your JSON files
DATA_FOLDER = r"C:\Users\user\Desktop\tasks\End_To_End_Medical_Intelligence_Platform\data\raw\telegram_messages\2025-07-10"

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()



# Read and combine all JSON files into one DataFrame
all_data = []

for file in os.listdir(DATA_FOLDER):
            with open(os.path.join(DATA_FOLDER, file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    data = [data]
                all_data.extend(data)
                
    

# Convert to DataFrame
df = pd.json_normalize(all_data)
df.columns = [col.replace(".", "_") for col in df.columns]  # Sanitize column names



# Rename conflicting 'id' column from JSON to avoid clash with SERIAL PRIMARY KEY
if 'id' in df.columns:
    df.rename(columns={'id': 'json_id'}, inplace=True)

# Create table if not exists
columns = df.columns
column_defs = ", ".join(f"{col} TEXT" for col in columns)

create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.{TABLE_NAME} (
        id SERIAL PRIMARY KEY,
        {column_defs}
    );
"""
cursor.execute(create_table_sql)

# Insert data
for _, row in df.iterrows():
    insert_sql = sql.SQL("INSERT INTO {}.{} ({}) VALUES ({})").format(
        sql.Identifier(SCHEMA_NAME),
        sql.Identifier(TABLE_NAME),
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )
    cursor.execute(insert_sql, tuple(str(row[col]) for col in columns))

# Finalize
conn.commit()
cursor.close()
conn.close()



