from __future__ import annotations

import os
import sys

import psycopg
from dotenv import load_dotenv


load_dotenv()


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}


def check_count(cur, table: str) -> None:
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    count = cur.fetchone()[0]

    if count <= 0:
        raise AssertionError(f"{table} is empty")

    print(f"PASS | {table:<35} rows={count:,}")


def check_zero(cur, name: str, query: str) -> None:
    cur.execute(query)
    value = cur.fetchone()[0]

    if value != 0:
        raise AssertionError(f"{name}: expected 0, got {value}")

    print(f"PASS | {name}")


def main() -> None:
    print("=" * 70)
    print("EODIP - DATA QUALITY VALIDATION")
    print("=" * 70)

    try:
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:

                print("\n[1] TABLE AVAILABILITY")
                tables = [
                    "raw.customers",
                    "raw.products",
                    "raw.suppliers",
                    "raw.warehouses",
                    "raw.sales",
                    "raw.purchases",
                    "staging.customers",
                    "staging.products",
                    "staging.suppliers",
                    "staging.warehouses",
                    "staging.sales",
                    "staging.purchases",
                    "dwh.dim_date",
                    "dwh.dim_product",
                    "dwh.dim_customer",
                    "dwh.dim_supplier",
                    "dwh.dim_warehouse",
                    "dwh.fact_sales",
                    "dwh.fact_purchases",
                ]

                for table in tables:
                    check_count(cur, table)

                print("\n[2] REFERENTIAL INTEGRITY")

                check_zero(
                    cur,
                    "Orphan sales -> date",
                    """
                    SELECT COUNT(*)
                    FROM dwh.fact_sales f
                    LEFT JOIN dwh.dim_date d
                        ON f.date_key = d.date_key
                    WHERE d.date_key IS NULL
                    """,
                )

                check_zero(
                    cur,
                    "Orphan sales -> product",
                    """
                    SELECT COUNT(*)
                    FROM dwh.fact_sales f
                    LEFT JOIN dwh.dim_product d
                        ON f.product_key = d.product_key
                    WHERE d.product_key IS NULL
                    """,
                )

                check_zero(
                    cur,
                    "Orphan sales -> customer",
                    """
                    SELECT COUNT(*)
                    FROM dwh.fact_sales f
                    LEFT JOIN dwh.dim_customer d
                        ON f.customer_key = d.customer_key
                    WHERE d.customer_key IS NULL
                    """,
                )

                check_zero(
                    cur,
                    "Orphan sales -> warehouse",
                    """
                    SELECT COUNT(*)
                    FROM dwh.fact_sales f
                    LEFT JOIN dwh.dim_warehouse d
                        ON f.warehouse_key = d.warehouse_key
                    WHERE d.warehouse_key IS NULL
                    """,
                )

                check_zero(
                    cur,
                    "Orphan purchases -> date",
                    """
                    SELECT COUNT(*)
                    FROM dwh.fact_purchases f
                    LEFT JOIN dwh.dim_date d
                        ON f.date_key = d.date_key
                    WHERE d.date_key IS NULL
                    """,
                )

                check_zero(
                    cur,
                    "Orphan purchases -> product",
                    """
                    SELECT COUNT(*)
                    FROM dwh.fact_purchases f
                    LEFT JOIN dwh.dim_product d
                        ON f.product_key = d.product_key
                    WHERE d.product_key IS NULL
                    """,
                )

                check_zero(
                    cur,
                    "Orphan purchases -> supplier",
                    """
                    SELECT COUNT(*)
                    FROM dwh.fact_purchases f
                    LEFT JOIN dwh.dim_supplier d
                        ON f.supplier_key = d.supplier_key
                    WHERE d.supplier_key IS NULL
                    """,
                )

                check_zero(
                    cur,
                    "Orphan purchases -> warehouse",
                    """
                    SELECT COUNT(*)
                    FROM dwh.fact_purchases f
                    LEFT JOIN dwh.dim_warehouse d
                        ON f.warehouse_key = d.warehouse_key
                    WHERE d.warehouse_key IS NULL
                    """,
                )

                print("\n[3] CRITICAL NULL CHECKS")

                check_zero(
                    cur,
                    "NULL sales date_key",
                    """
                    SELECT COUNT(*)
                    FROM dwh.fact_sales
                    WHERE date_key IS NULL
                    """,
                )

                check_zero(
                    cur,
                    "NULL sales product_key",
                    """
                    SELECT COUNT(*)
                    FROM dwh.fact_sales
                    WHERE product_key IS NULL
                    """,
                )

                check_zero(
                    cur,
                    "NULL purchase date_key",
                    """
                    SELECT COUNT(*)
                    FROM dwh.fact_purchases
                    WHERE date_key IS NULL
                    """,
                )

                check_zero(
                    cur,
                    "NULL purchase product_key",
                    """
                    SELECT COUNT(*)
                    FROM dwh.fact_purchases
                    WHERE product_key IS NULL
                    """,
                )

                print("\n[4] BI VIEWS")

                check_count(cur, "bi.vw_sales_performance")
                check_count(cur, "bi.vw_purchase_performance")
                check_count(cur, "bi.vw_supply_chain_performance")

        print("\n" + "=" * 70)
        print("EODIP VALIDATION COMPLETED SUCCESSFULLY")
        print("=" * 70)

    except Exception as exc:
        print("\n" + "=" * 70)
        print("EODIP VALIDATION FAILED")
        print(f"ERROR: {exc}")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()