from __future__ import annotations

import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


connection = psycopg.connect(
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    dbname=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
)

print("PostgreSQL connection successful.")

connection.close()