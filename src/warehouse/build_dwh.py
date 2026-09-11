"""
EODIP - STAGING -> DATA WAREHOUSE

Creates and loads a star-schema analytical warehouse.

Schemas:
    staging = cleaned operational data
    dwh     = dimensional analytical model

Dimensions:
    dim_date
    dim_product
    dim_customer
    dim_supplier
    dim_warehouse

Facts:
    fact_sales
    fact_purchases
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


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================
# DATABASE
# ============================================================

def get_engine():
    """Create PostgreSQL SQLAlchemy engine."""

    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME", "eodip")
    username = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD")

    if not password:
        raise ValueError(
            "DB_PASSWORD is missing from .env"
        )

    return create_engine(
        (
            f"postgresql+psycopg://"
            f"{username}:{password}"
            f"@{host}:{port}/{database}"
        ),
        pool_pre_ping=True,
    )


# ============================================================
# LOAD STAGING
# ============================================================

def load_table(
    engine,
    table_name: str,
) -> pd.DataFrame:
    """Load a staging table."""

    query = text(
        f'SELECT * FROM staging."{table_name}"'
    )

    logger.info(
        "Loading staging.%s",
        table_name,
    )

    return pd.read_sql_query(
        query,
        engine,
    )


# ============================================================
# DIMENSION: DATE
# ============================================================

def build_dim_date(
    sales: pd.DataFrame,
    purchases: pd.DataFrame,
) -> pd.DataFrame:
    """Build calendar dimension."""

    sale_dates = pd.to_datetime(
        sales["sale_date"],
        errors="coerce",
    )

    order_dates = pd.to_datetime(
        purchases["order_date"],
        errors="coerce",
    )

    received_dates = pd.to_datetime(
        purchases["received_date"],
        errors="coerce",
    )

    all_dates = pd.concat(
        [
            sale_dates,
            order_dates,
            received_dates,
        ],
        ignore_index=True,
    ).dropna()

    min_date = all_dates.min().normalize()
    max_date = all_dates.max().normalize()

    dates = pd.date_range(
        start=min_date,
        end=max_date,
        freq="D",
    )

    dim_date = pd.DataFrame(
        {
            "date": dates,
        }
    )

    dim_date["date_key"] = (
        dim_date["date"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    dim_date["year"] = (
        dim_date["date"].dt.year
    )

    dim_date["quarter"] = (
        dim_date["date"].dt.quarter
    )

    dim_date["month"] = (
        dim_date["date"].dt.month
    )

    dim_date["month_name"] = (
        dim_date["date"].dt.month_name()
    )

    dim_date["week"] = (
        dim_date["date"].dt.isocalendar().week.astype(int)
    )

    dim_date["day"] = (
        dim_date["date"].dt.day
    )

    dim_date["day_name"] = (
        dim_date["date"].dt.day_name()
    )

    dim_date["is_weekend"] = (
        dim_date["date"].dt.dayofweek >= 5
    )

    return dim_date[
        [
            "date_key",
            "date",
            "year",
            "quarter",
            "month",
            "month_name",
            "week",
            "day",
            "day_name",
            "is_weekend",
        ]
    ]


# ============================================================
# DIMENSIONS
# ============================================================

def build_dim_product(
    products: pd.DataFrame,
) -> pd.DataFrame:
    """Build product dimension."""

    df = products.copy()

    df["product_key"] = (
        df["product_id"]
        .astype("category")
        .cat.codes
        + 1
    )

    return df[
        [
            "product_key",
            "product_id",
            "product_name",
            "category",
            "unit_cost",
            "unit_price",
        ]
    ]


def build_dim_customer(
    customers: pd.DataFrame,
) -> pd.DataFrame:
    """Build customer dimension."""

    df = customers.copy()

    df["customer_key"] = (
        df["customer_id"]
        .astype("category")
        .cat.codes
        + 1
    )

    return df[
        [
            "customer_key",
            "customer_id",
            "customer_name",
            "country",
            "city",
            "customer_segment",
        ]
    ]


def build_dim_supplier(
    suppliers: pd.DataFrame,
) -> pd.DataFrame:
    """Build supplier dimension."""

    df = suppliers.copy()

    df["supplier_key"] = (
        df["supplier_id"]
        .astype("category")
        .cat.codes
        + 1
    )

    return df[
        [
            "supplier_key",
            "supplier_id",
            "supplier_name",
            "country",
            "city",
            "status",
        ]
    ]


def build_dim_warehouse(
    warehouses: pd.DataFrame,
) -> pd.DataFrame:
    """Build warehouse dimension."""

    df = warehouses.copy()

    df["warehouse_key"] = (
        df["warehouse_id"]
        .astype("category")
        .cat.codes
        + 1
    )

    return df[
        [
            "warehouse_key",
            "warehouse_id",
            "warehouse_name",
            "city",
            "country",
            "capacity",
        ]
    ]


# ============================================================
# FACT SALES
# ============================================================

def build_fact_sales(
    sales: pd.DataFrame,
    dim_date: pd.DataFrame,
    dim_product: pd.DataFrame,
    dim_customer: pd.DataFrame,
    dim_warehouse: pd.DataFrame,
) -> pd.DataFrame:
    """Build sales fact table."""

    df = sales.copy()

    df["sale_date"] = pd.to_datetime(
        df["sale_date"]
    )

    # Date surrogate key
    df["date_key"] = (
        df["sale_date"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    # Dimension mappings
    product_map = dict(
        zip(
            dim_product["product_id"],
            dim_product["product_key"],
        )
    )

    customer_map = dict(
        zip(
            dim_customer["customer_id"],
            dim_customer["customer_key"],
        )
    )

    warehouse_map = dict(
        zip(
            dim_warehouse["warehouse_id"],
            dim_warehouse["warehouse_key"],
        )
    )

    df["product_key"] = (
        df["product_id"]
        .map(product_map)
    )

    df["customer_key"] = (
        df["customer_id"]
        .map(customer_map)
    )

    df["warehouse_key"] = (
        df["warehouse_id"]
        .map(warehouse_map)
    )

    df["sales_key"] = range(
        1,
        len(df) + 1,
    )

    return df[
        [
            "sales_key",
            "date_key",
            "product_key",
            "customer_key",
            "warehouse_key",
            "sale_id",
            "quantity",
            "unit_price",
            "discount",
            "gross_amount",
            "discount_amount",
            "net_amount",
        ]
    ]


# ============================================================
# FACT PURCHASES
# ============================================================

def build_fact_purchases(
    purchases: pd.DataFrame,
    dim_date: pd.DataFrame,
    dim_product: pd.DataFrame,
    dim_supplier: pd.DataFrame,
    dim_warehouse: pd.DataFrame,
) -> pd.DataFrame:
    """Build purchases fact table."""

    df = purchases.copy()

    df["order_date"] = pd.to_datetime(
        df["order_date"]
    )

    df["date_key"] = (
        df["order_date"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    product_map = dict(
        zip(
            dim_product["product_id"],
            dim_product["product_key"],
        )
    )

    supplier_map = dict(
        zip(
            dim_supplier["supplier_id"],
            dim_supplier["supplier_key"],
        )
    )

    warehouse_map = dict(
        zip(
            dim_warehouse["warehouse_id"],
            dim_warehouse["warehouse_key"],
        )
    )

    df["product_key"] = (
        df["product_id"]
        .map(product_map)
    )

    df["supplier_key"] = (
        df["supplier_id"]
        .map(supplier_map)
    )

    df["warehouse_key"] = (
        df["warehouse_id"]
        .map(warehouse_map)
    )

    df["received_date"] = pd.to_datetime(
        df["received_date"],
        errors="coerce",
    )

    df["expected_date"] = pd.to_datetime(
        df["expected_date"],
        errors="coerce",
    )

    df["purchase_key"] = range(
        1,
        len(df) + 1,
    )

    return df[
        [
            "purchase_key",
            "date_key",
            "product_key",
            "supplier_key",
            "warehouse_key",
            "purchase_id",
            "quantity",
            "unit_cost",
            "purchase_amount",
            "order_date",
            "expected_date",
            "received_date",
            "delivery_delay_days",
            "delivery_status",
        ]
    ]


# ============================================================
# WRITE DWH
# ============================================================

def write_table(
    engine,
    table_name: str,
    df: pd.DataFrame,
) -> None:
    """Write dataframe to DWH."""

    df.to_sql(
        table_name,
        engine,
        schema="dwh",
        if_exists="replace",    
        index=False,
        method="multi",
        chunksize=2000,
        )

    logger.info(
        "dwh.%s loaded | %s rows",
        table_name,
        f"{len(df):,}",
    )


# ============================================================
# ADD CONSTRAINTS
# ============================================================

def create_constraints(
    engine,
) -> None:
    """Add primary keys and analytical indexes."""

    statements = [
        """
        ALTER TABLE dwh.dim_date
        ADD PRIMARY KEY (date_key)
        """,

        """
        ALTER TABLE dwh.dim_product
        ADD PRIMARY KEY (product_key)
        """,

        """
        ALTER TABLE dwh.dim_customer
        ADD PRIMARY KEY (customer_key)
        """,

        """
        ALTER TABLE dwh.dim_supplier
        ADD PRIMARY KEY (supplier_key)
        """,

        """
        ALTER TABLE dwh.dim_warehouse
        ADD PRIMARY KEY (warehouse_key)
        """,

        """
        ALTER TABLE dwh.fact_sales
        ADD PRIMARY KEY (sales_key)
        """,

        """
        ALTER TABLE dwh.fact_purchases
        ADD PRIMARY KEY (purchase_key)
        """,

        """
        CREATE INDEX idx_fact_sales_date
        ON dwh.fact_sales(date_key)
        """,

        """
        CREATE INDEX idx_fact_sales_product
        ON dwh.fact_sales(product_key)
        """,

        """
        CREATE INDEX idx_fact_sales_customer
        ON dwh.fact_sales(customer_key)
        """,

        """
        CREATE INDEX idx_fact_purchases_date
        ON dwh.fact_purchases(date_key)
        """,

        """
        CREATE INDEX idx_fact_purchases_product
        ON dwh.fact_purchases(product_key)
        """,

        """
        CREATE INDEX idx_fact_purchases_supplier
        ON dwh.fact_purchases(supplier_key)
        """,
    ]

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(
                text(statement)
            )

    logger.info(
        "DWH constraints and indexes created."
    )


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    """Execute STAGING -> DWH pipeline."""

    logger.info(
        "Starting STAGING -> DWH pipeline."
    )

    engine = get_engine()

    # --------------------------------------------------------
    # Schema
    # --------------------------------------------------------

    with engine.begin() as connection:
        connection.execute(
            text(
                "CREATE SCHEMA IF NOT EXISTS dwh"
            )
        )

    logger.info(
        "DWH schema verified."
    )

    # --------------------------------------------------------
    # Load staging
    # --------------------------------------------------------

    products = load_table(
        engine,
        "products",
    )

    customers = load_table(
        engine,
        "customers",
    )

    suppliers = load_table(
        engine,
        "suppliers",
    )

    warehouses = load_table(
        engine,
        "warehouses",
    )

    sales = load_table(
        engine,
        "sales",
    )

    purchases = load_table(
        engine,
        "purchases",
    )

    # --------------------------------------------------------
    # Build dimensions
    # --------------------------------------------------------

    logger.info(
        "Building dimensions."
    )

    dim_date = build_dim_date(
        sales,
        purchases,
    )

    dim_product = build_dim_product(
        products
    )

    dim_customer = build_dim_customer(
        customers
    )

    dim_supplier = build_dim_supplier(
        suppliers
    )

    dim_warehouse = build_dim_warehouse(
        warehouses
    )

    # --------------------------------------------------------
    # Build facts
    # --------------------------------------------------------

    logger.info(
        "Building fact tables."
    )

    fact_sales = build_fact_sales(
        sales,
        dim_date,
        dim_product,
        dim_customer,
        dim_warehouse,
    )

    fact_purchases = build_fact_purchases(
        purchases,
        dim_date,
        dim_product,
        dim_supplier,
        dim_warehouse,
    )

    with engine.begin() as conn:
        # Remove DWH views before replacing DWH tables
        conn.execute(text("DROP VIEW IF EXISTS dwh.vw_supply_chain_performance"))
        conn.execute(text("DROP VIEW IF EXISTS dwh.vw_purchase_performance"))
        conn.execute(text("DROP VIEW IF EXISTS dwh.vw_sales_performance"))

        # Remove BI views before rebuilding the DWH

        conn.execute(text("DROP VIEW IF EXISTS bi.vw_supply_chain_performance"))
        conn.execute(text("DROP VIEW IF EXISTS bi.vw_purchase_performance"))
        conn.execute(text("DROP VIEW IF EXISTS bi.vw_sales_performance"))

    # --------------------------------------------------------
    # Write dimensions
    # --------------------------------------------------------

    write_table(
        engine,
        "dim_date",
        dim_date,
    )

    write_table(
        engine,
        "dim_product",
        dim_product,
    )

    write_table(
        engine,
        "dim_customer",
        dim_customer,
    )

    write_table(
        engine,
        "dim_supplier",
        dim_supplier,
    )

    write_table(
        engine,
        "dim_warehouse",
        dim_warehouse,
    )

    # --------------------------------------------------------
    # Write facts
    # --------------------------------------------------------

    write_table(
        engine,
        "fact_sales",
        fact_sales,
    )

    write_table(
        engine,
        "fact_purchases",
        fact_purchases,
    )

    # --------------------------------------------------------
    # Constraints
    # --------------------------------------------------------

    create_constraints(
        engine
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("=" * 80)
    print("EODIP DATA WAREHOUSE SUMMARY")
    print("=" * 80)

    print(
        f"dim_date        | {len(dim_date):>10,} rows"
    )

    print(
        f"dim_product     | {len(dim_product):>10,} rows"
    )

    print(
        f"dim_customer    | {len(dim_customer):>10,} rows"
    )

    print(
        f"dim_supplier    | {len(dim_supplier):>10,} rows"
    )

    print(
        f"dim_warehouse   | {len(dim_warehouse):>10,} rows"
    )

    print(
        f"fact_sales      | {len(fact_sales):>10,} rows"
    )

    print(
        f"fact_purchases  | {len(fact_purchases):>10,} rows"
    )

    print("=" * 80)

    logger.info(
        "STAGING -> DWH pipeline completed successfully."
    )


if __name__ == "__main__":
    main()