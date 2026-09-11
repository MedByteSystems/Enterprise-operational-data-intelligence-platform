from __future__ import annotations

import logging
import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"

load_dotenv(BASE_DIR / ".env")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


REQUIRED_ENV_VARS = [
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
]


SOURCE_FILES = [
    "suppliers.csv",
    "products.csv",
    "customers.csv",
    "warehouses.csv",
    "purchases.csv",
    "sales.csv",
]


def validate_environment() -> None:
    missing = [
        variable
        for variable in REQUIRED_ENV_VARS
        if not os.getenv(variable)
    ]

    if missing:
        raise RuntimeError(
            "Missing environment variables: "
            + ", ".join(missing)
        )


def get_database_config() -> dict[str, object]:
    validate_environment()

    return {
        "host": os.environ["DB_HOST"],
        "port": int(os.environ["DB_PORT"]),
        "dbname": os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
    }


def filename_to_table(filename: str) -> str:
    return Path(filename).stem.lower()


def quote_identifier(identifier: str) -> str:
    escaped = identifier.replace('"', '""')
    return f'"{escaped}"'


def create_raw_schema(conn: psycopg.Connection) -> None:
    with conn.cursor() as cursor:
        cursor.execute(
            "CREATE SCHEMA IF NOT EXISTS raw"
        )

    conn.commit()
    logger.info("RAW schema verified.")


def load_csv_to_raw(
    conn: psycopg.Connection,
    filename: str,
) -> None:

    source_path = RAW_DIR / filename

    if not source_path.exists():
        raise FileNotFoundError(
            f"Source file not found: {source_path}"
        )

    table_name = filename_to_table(filename)

    logger.info("Reading source file: %s", filename)

    dataframe = pd.read_csv(source_path)

    if dataframe.empty:
        logger.warning(
            "Source file %s is empty.",
            filename,
        )
        return

    column_definitions = ", ".join(
        f"{quote_identifier(column)} TEXT"
        for column in dataframe.columns
    )

    # IMPORTANT:
    # The table is explicitly created inside the RAW schema.
    qualified_table = (
        f"raw.{quote_identifier(table_name)}"
    )

    create_table_sql = f"""
        CREATE TABLE {qualified_table} (
            {column_definitions}
        )
    """

    quoted_columns = ", ".join(
        quote_identifier(column)
        for column in dataframe.columns
    )

    placeholders = ", ".join(
        ["%s"] * len(dataframe.columns)
    )

    insert_sql = f"""
        INSERT INTO {qualified_table} ({quoted_columns})
        VALUES ({placeholders})
    """

    records = [
        tuple(
            None if pd.isna(value) else str(value)
            for value in row
        )
        for row in dataframe.itertuples(
            index=False,
            name=None,
        )
    ]

    try:
        with conn.cursor() as cursor:

            cursor.execute(
                f"DROP TABLE IF EXISTS {qualified_table} CASCADE"
            )

            cursor.execute(create_table_sql)

            cursor.executemany(
                insert_sql,
                records,
            )

        conn.commit()

        logger.info(
            "Loaded %s | %s rows | raw.%s",
            filename,
            f"{len(dataframe):,}",
            table_name,
        )

    except Exception:
        conn.rollback()

        logger.exception(
            "Failed to load %s",
            filename,
        )

        raise


def run_ingestion() -> None:

    logger.info(
        "Starting RAW ingestion pipeline."
    )

    if not RAW_DIR.exists():
        raise FileNotFoundError(
            f"RAW directory not found: {RAW_DIR}"
        )

    database_config = get_database_config()

    logger.info(
        "Source directory: %s",
        RAW_DIR,
    )

    with psycopg.connect(
        **database_config
    ) as connection:

        create_raw_schema(connection)

        for filename in SOURCE_FILES:
            load_csv_to_raw(
                connection,
                filename,
            )

    logger.info(
        "RAW ingestion completed successfully."
    )


if __name__ == "__main__":
    run_ingestion()