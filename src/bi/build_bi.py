from __future__ import annotations

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}


SQL_FILES = [
    PROJECT_ROOT / "sql" / "bi" / "vw_sales_performance.sql",
    PROJECT_ROOT / "sql" / "bi" / "vw_purchase_performance.sql",
    PROJECT_ROOT / "sql" / "bi" / "vw_supply_chain_performance.sql",
]


def main() -> None:
    print("=" * 70)
    print("EODIP - BI LAYER")
    print("=" * 70)

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:

            cur.execute("CREATE SCHEMA IF NOT EXISTS bi")

            for sql_file in SQL_FILES:
                print(f"Loading: {sql_file.name}")

                if not sql_file.exists():
                    raise FileNotFoundError(
                        f"SQL file not found: {sql_file}"
                    )

                sql = sql_file.read_text(encoding="utf-8")

                cur.execute(sql)

                print(f"SUCCESS: {sql_file.name}")

        conn.commit()

    print("=" * 70)
    print("BI LAYER COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()