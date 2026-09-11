"""
EODIP - RAW -> STAGING Transformation

Purpose:
    Clean and standardize RAW data before loading the Data Warehouse.

Flow:
    PostgreSQL RAW
        ↓
    Cleaning / standardization
        ↓
    PostgreSQL STAGING

STAGING tables:
    staging.products
    staging.customers
    staging.suppliers
    staging.warehouses
    staging.sales
    staging.purchases
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_engine():
    """Create SQLAlchemy PostgreSQL engine."""

    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME", "eodip")
    username = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD")

    if not password:
        raise ValueError(
            "DB_PASSWORD is missing from .env"
        )

    database_url = (
        f"postgresql+psycopg://"
        f"{username}:{password}"
        f"@{host}:{port}/{database}"
    )

    return create_engine(
        database_url,
        pool_pre_ping=True,
    )


# ============================================================
# RAW LOADING
# ============================================================

def load_raw_table(
    engine,
    table_name: str,
) -> pd.DataFrame:
    """Load one table from the RAW schema."""

    query = text(
        f'SELECT * FROM raw."{table_name}"'
    )

    logger.info(
        "Loading raw.%s",
        table_name,
    )

    return pd.read_sql_query(
        query,
        engine,
    )


# ============================================================
# DIMENSIONS
# ============================================================

def prepare_products(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Clean products dimension."""

    df = df.copy()

    before = len(df)

    # Remove records with missing category.
    df = df.dropna(
        subset=["category"]
    )

    # Keep one record per business key.
    df = df.drop_duplicates(
        subset=["product_id"]
    )

    # Numeric standardization.
    df["unit_cost"] = pd.to_numeric(
        df["unit_cost"],
        errors="coerce",
    )

    df["unit_price"] = pd.to_numeric(
        df["unit_price"],
        errors="coerce",
    )

    logger.info(
        "products: %s -> %s rows",
        f"{before:,}",
        f"{len(df):,}",
    )

    return df.reset_index(drop=True)


def prepare_customers(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Clean customers dimension."""

    df = df.copy()

    before = len(df)

    df = df.drop_duplicates(
        subset=["customer_id"]
    )

    logger.info(
        "customers: %s -> %s rows",
        f"{before:,}",
        f"{len(df):,}",
    )

    return df.reset_index(drop=True)


def prepare_suppliers(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Clean suppliers dimension."""

    df = df.copy()

    before = len(df)

    df = df.drop_duplicates(
        subset=["supplier_id"]
    )

    logger.info(
        "suppliers: %s -> %s rows",
        f"{before:,}",
        f"{len(df):,}",
    )

    return df.reset_index(drop=True)


def prepare_warehouses(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Clean warehouses dimension."""

    df = df.copy()

    before = len(df)

    df = df.drop_duplicates(
        subset=["warehouse_id"]
    )

    df["capacity"] = pd.to_numeric(
        df["capacity"],
        errors="coerce",
    )

    logger.info(
        "warehouses: %s -> %s rows",
        f"{before:,}",
        f"{len(df):,}",
    )

    return df.reset_index(drop=True)


# ============================================================
# SALES
# ============================================================

def prepare_sales(
    df: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame,
    warehouses: pd.DataFrame,
) -> pd.DataFrame:
    """
    Clean sales fact data.

    Rules:
    - customer_id cannot be NULL
    - references must exist
    - quantity must be > 0
    - dates must be valid
    - duplicate records are removed
    """

    df = df.copy()

    before = len(df)

    # --------------------------------------------------------
    # Type normalization
    # --------------------------------------------------------

    df["sale_date"] = pd.to_datetime(
        df["sale_date"],
        errors="coerce",
    )

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce",
    )

    df["unit_price"] = pd.to_numeric(
        df["unit_price"],
        errors="coerce",
    )

    df["discount"] = pd.to_numeric(
        df["discount"],
        errors="coerce",
    ).fillna(0)

    # --------------------------------------------------------
    # Valid reference sets
    # --------------------------------------------------------

    valid_customers = set(
        customers["customer_id"]
        .dropna()
        .astype(str)
    )

    valid_products = set(
        products["product_id"]
        .dropna()
        .astype(str)
    )

    valid_warehouses = set(
        warehouses["warehouse_id"]
        .dropna()
        .astype(str)
    )

    # --------------------------------------------------------
    # Data quality filter
    # --------------------------------------------------------

    mask = (
        df["customer_id"].notna()
        & df["product_id"].notna()
        & df["warehouse_id"].notna()
        & df["sale_date"].notna()
        & (df["quantity"] > 0)
        & df["customer_id"]
        .astype(str)
        .isin(valid_customers)
        & df["product_id"]
        .astype(str)
        .isin(valid_products)
        & df["warehouse_id"]
        .astype(str)
        .isin(valid_warehouses)
    )

    df = df.loc[mask].copy()

    # --------------------------------------------------------
    # Remove complete duplicates
    # --------------------------------------------------------

    df = df.drop_duplicates()

    # --------------------------------------------------------
    # Derived business metrics
    # --------------------------------------------------------

    df["gross_amount"] = (
        df["quantity"]
        * df["unit_price"]
    )

    df["discount_amount"] = (
        df["gross_amount"]
        * df["discount"]
    )

    df["net_amount"] = (
        df["gross_amount"]
        - df["discount_amount"]
    )

    # --------------------------------------------------------
    # Final ordering
    # --------------------------------------------------------

    df = (
        df.sort_values("sale_date")
        .reset_index(drop=True)
    )

    logger.info(
        "sales: %s -> %s rows",
        f"{before:,}",
        f"{len(df):,}",
    )

    return df


# ============================================================
# PURCHASES
# ============================================================

def prepare_purchases(
    df: pd.DataFrame,
    suppliers: pd.DataFrame,
    products: pd.DataFrame,
    warehouses: pd.DataFrame,
) -> pd.DataFrame:
    """
    Clean purchase fact data.

    Rules:
    - supplier reference must exist
    - product reference must exist
    - warehouse reference must exist
    - quantity must be positive
    - order date must be valid
    - received date must be >= order date
    """

    df = df.copy()

    before = len(df)

    # --------------------------------------------------------
    # Type normalization
    # --------------------------------------------------------

    for column in [
        "order_date",
        "expected_date",
        "received_date",
    ]:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce",
        )

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce",
    )

    df["unit_cost"] = pd.to_numeric(
        df["unit_cost"],
        errors="coerce",
    )

    # --------------------------------------------------------
    # Valid references
    # --------------------------------------------------------

    valid_suppliers = set(
        suppliers["supplier_id"]
        .dropna()
        .astype(str)
    )

    valid_products = set(
        products["product_id"]
        .dropna()
        .astype(str)
    )

    valid_warehouses = set(
        warehouses["warehouse_id"]
        .dropna()
        .astype(str)
    )

    # --------------------------------------------------------
    # Data quality filter
    # --------------------------------------------------------

    mask = (
        df["supplier_id"].notna()
        & df["product_id"].notna()
        & df["warehouse_id"].notna()
        & df["order_date"].notna()
        & (df["quantity"] > 0)
        & (df["unit_cost"] >= 0)
        & df["supplier_id"]
        .astype(str)
        .isin(valid_suppliers)
        & df["product_id"]
        .astype(str)
        .isin(valid_products)
        & df["warehouse_id"]
        .astype(str)
        .isin(valid_warehouses)
        & (
            df["received_date"].isna()
            | (
                df["received_date"]
                >= df["order_date"]
            )
        )
    )

    df = df.loc[mask].copy()

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    df = df.drop_duplicates()

    # --------------------------------------------------------
    # Derived business metrics
    # --------------------------------------------------------

    df["purchase_amount"] = (
        df["quantity"]
        * df["unit_cost"]
    )

    df["delivery_delay_days"] = (
        df["received_date"]
        - df["expected_date"]
    ).dt.days

    df["delivery_status"] = df[
        "delivery_delay_days"
    ].apply(
        lambda value:
            "LATE"
            if pd.notna(value) and value > 0
            else "ON_TIME"
    )

    # --------------------------------------------------------
    # Final ordering
    # --------------------------------------------------------

    df = (
        df.sort_values("order_date")
        .reset_index(drop=True)
    )

    logger.info(
        "purchases: %s -> %s rows",
        f"{before:,}",
        f"{len(df):,}",
    )

    return df


# ============================================================
# DATABASE WRITE
# ============================================================

def write_staging_table(
    engine,
    table_name: str,
    df: pd.DataFrame,
) -> None:
    """Write dataframe to staging schema."""

    df.to_sql(
        table_name,
        engine,
        schema="staging",
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=5000,
    )

    logger.info(
        "staging.%s loaded | %s rows",
        table_name,
        f"{len(df):,}",
    )


# ============================================================
# MAIN PIPELINE
# ============================================================

def main() -> None:
    """Execute complete RAW -> STAGING pipeline."""

    logger.info(
        "Starting RAW -> STAGING transformation."
    )

    engine = get_engine()

    # --------------------------------------------------------
    # Create staging schema
    # --------------------------------------------------------

    with engine.begin() as connection:
        connection.execute(
            text(
                "CREATE SCHEMA IF NOT EXISTS staging"
            )
        )

    logger.info(
        "STAGING schema verified."
    )

    # --------------------------------------------------------
    # Load RAW tables
    # --------------------------------------------------------

    raw_products = load_raw_table(
        engine,
        "products",
    )

    raw_customers = load_raw_table(
        engine,
        "customers",
    )

    raw_suppliers = load_raw_table(
        engine,
        "suppliers",
    )

    raw_warehouses = load_raw_table(
        engine,
        "warehouses",
    )

    raw_sales = load_raw_table(
        engine,
        "sales",
    )

    raw_purchases = load_raw_table(
        engine,
        "purchases",
    )

    # --------------------------------------------------------
    # Prepare dimensions
    # --------------------------------------------------------

    products = prepare_products(
        raw_products
    )

    customers = prepare_customers(
        raw_customers
    )

    suppliers = prepare_suppliers(
        raw_suppliers
    )

    warehouses = prepare_warehouses(
        raw_warehouses
    )

    # --------------------------------------------------------
    # Prepare facts
    # --------------------------------------------------------

    sales = prepare_sales(
        raw_sales,
        customers,
        products,
        warehouses,
    )

    purchases = prepare_purchases(
        raw_purchases,
        suppliers,
        products,
        warehouses,
    )

    # --------------------------------------------------------
    # Write dimensions
    # --------------------------------------------------------

    write_staging_table(
        engine,
        "products",
        products,
    )

    write_staging_table(
        engine,
        "customers",
        customers,
    )

    write_staging_table(
        engine,
        "suppliers",
        suppliers,
    )

    write_staging_table(
        engine,
        "warehouses",
        warehouses,
    )

    # --------------------------------------------------------
    # Write facts
    # --------------------------------------------------------

    write_staging_table(
        engine,
        "sales",
        sales,
    )

    write_staging_table(
        engine,
        "purchases",
        purchases,
    )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print()
    print("=" * 80)
    print("EODIP STAGING SUMMARY")
    print("=" * 80)

    print(
        f"products     | {len(products):>10,} rows"
    )

    print(
        f"customers    | {len(customers):>10,} rows"
    )

    print(
        f"suppliers    | {len(suppliers):>10,} rows"
    )

    print(
        f"warehouses   | {len(warehouses):>10,} rows"
    )

    print(
        f"sales        | {len(sales):>10,} rows"
    )

    print(
        f"purchases    | {len(purchases):>10,} rows"
    )

    print("=" * 80)

    logger.info(
        "RAW -> STAGING transformation completed successfully."
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()