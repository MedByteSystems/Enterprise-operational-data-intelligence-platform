"""
EODIP - RAW Data Quality Validation

Validates data ingested into the PostgreSQL RAW schema.

Quality checks:
- NOT NULL constraints
- Positive numeric values
- Duplicate records
- Foreign-key/reference integrity
- Date consistency

Outputs:
    data/quality/quality_report.csv
    data/quality/quality_summary.csv
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
QUALITY_DIR = PROJECT_ROOT / "data" / "quality"

QUALITY_REPORT_PATH = QUALITY_DIR / "quality_report.csv"
QUALITY_SUMMARY_PATH = QUALITY_DIR / "quality_summary.csv"

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
# DATABASE
# ============================================================

def get_database_url() -> str:
    """
    Build the PostgreSQL SQLAlchemy connection URL from .env.
    """

    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME", "eodip")
    username = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD")

    if not password:
        raise ValueError(
            "DB_PASSWORD is missing from .env"
        )

    return (
        f"postgresql+psycopg://"
        f"{username}:{password}"
        f"@{host}:{port}/{database}"
    )


def get_engine():
    """
    Create SQLAlchemy engine.
    """

    database_url = get_database_url()

    return create_engine(
        database_url,
        pool_pre_ping=True,
    )


# ============================================================
# HELPERS
# ============================================================

def load_table(
    engine,
    table_name: str,
) -> pd.DataFrame:
    """
    Load a table from the PostgreSQL RAW schema.
    """

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


def compute_distinct_row_quality(
    invalid_row_sets: list[set[int]],
    evaluated_rows: int,
) -> tuple[int, float]:
    """
    Compute data quality using DISTINCT affected rows.

    A row that violates several rules is counted only once.

    Parameters
    ----------
    invalid_row_sets:
        List of sets containing the dataframe indexes of invalid rows.

    evaluated_rows:
        Total number of rows evaluated.

    Returns
    -------
    tuple[int, float]
        distinct_invalid_rows, quality_percentage
    """

    if evaluated_rows <= 0:
        return 0, 100.0

    distinct_invalid_rows: set[int] = set()

    for row_set in invalid_row_sets:
        distinct_invalid_rows.update(row_set)

    invalid_count = len(distinct_invalid_rows)

    quality = max(
        0.0,
        100.0 * (
            1 - invalid_count / evaluated_rows
        ),
    )

    return invalid_count, round(quality, 2)


def build_rule_result(
    dataset: str,
    rule_name: str,
    evaluated_rows: int,
    invalid_indexes: set[int],
) -> dict:
    """
    Build one quality-rule result.
    """

    invalid_rows = len(invalid_indexes)

    quality = (
        100.0
        if evaluated_rows == 0
        else round(
            100.0
            * (1 - invalid_rows / evaluated_rows),
            2,
        )
    )

    status = (
        "PASS"
        if invalid_rows == 0
        else "FAIL"
    )

    return {
        "dataset": dataset,
        "rule": rule_name,
        "status": status,
        "invalid_rows": invalid_rows,
        "evaluated_rows": evaluated_rows,
        "row_quality_pct": quality,
    }


def build_summary(
    dataset: str,
    evaluated_rows: int,
    results: list[dict],
    invalid_row_sets: list[set[int]],
) -> dict:
    """
    Build dataset-level quality summary.

    The final score is based on DISTINCT rows affected
    by at least one validation rule.
    """

    failed_rules = sum(
        1
        for result in results
        if result["status"] == "FAIL"
    )

    distinct_invalid_rows, quality_score = (
        compute_distinct_row_quality(
            invalid_row_sets,
            evaluated_rows,
        )
    )

    if quality_score >= 99:
        quality_status = "EXCELLENT"
    elif quality_score >= 98:
        quality_status = "GOOD"
    elif quality_score >= 95:
        quality_status = "ACCEPTABLE"
    elif quality_score >= 90:
        quality_status = "WARNING"
    else:
        quality_status = "CRITICAL"

    return {
        "dataset": dataset,
        "evaluated_rows": evaluated_rows,
        "rules_checked": len(results),
        "failed_rules": failed_rules,
        "distinct_invalid_rows": distinct_invalid_rows,
        "quality_score_pct": quality_score,
        "quality_status": quality_status,
    }


# ============================================================
# QUALITY VALIDATION
# ============================================================

def validate_products(
    df: pd.DataFrame,
) -> tuple[list[dict], list[set[int]]]:
    """
    Validate PRODUCTS dataset.
    """

    results: list[dict] = []
    invalid_sets: list[set[int]] = []

    evaluated_rows = len(df)

    # --------------------------------------------------------
    # Rule 1 - category must not be NULL
    # --------------------------------------------------------

    invalid = set(
        df.index[
            df["category"].isna()
        ].tolist()
    )

    results.append(
        build_rule_result(
            "products",
            "category_not_null",
            evaluated_rows,
            invalid,
        )
    )

    invalid_sets.append(invalid)

    return results, invalid_sets


def validate_sales(
    df: pd.DataFrame,
    products: pd.DataFrame,
    customers: pd.DataFrame,
) -> tuple[list[dict], list[set[int]]]:
    """
    Validate SALES dataset.
    """

    results: list[dict] = []
    invalid_sets: list[set[int]] = []

    evaluated_rows = len(df)

    # --------------------------------------------------------
    # Rule 1 - customer_id must not be NULL
    # --------------------------------------------------------

    invalid = set(
        df.index[
            df["customer_id"].isna()
        ].tolist()
    )

    results.append(
        build_rule_result(
            "sales",
            "customer_id_not_null",
            evaluated_rows,
            invalid,
        )
    )

    invalid_sets.append(invalid)

    # --------------------------------------------------------
    # Rule 2 - quantity must be positive
    # --------------------------------------------------------

    quantity = pd.to_numeric(
        df["quantity"],
        errors="coerce",
    )

    invalid = set(
        df.index[
            quantity <= 0
        ].tolist()
    )

    results.append(
        build_rule_result(
            "sales",
            "quantity_positive",
            evaluated_rows,
            invalid,
        )
    )

    invalid_sets.append(invalid)

    # --------------------------------------------------------
    # Rule 3 - duplicate rows
    # --------------------------------------------------------

    duplicate_mask = df.duplicated(
        keep=False
    )

    invalid = set(
        df.index[
            duplicate_mask
        ].tolist()
    )

    results.append(
        build_rule_result(
            "sales",
            "duplicate_rows",
            evaluated_rows,
            invalid,
        )
    )

    invalid_sets.append(invalid)

    # --------------------------------------------------------
    # Rule 4 - customer reference must exist
    # --------------------------------------------------------

    valid_customer_ids = set(
        customers["customer_id"]
        .dropna()
        .astype(str)
    )

    customer_values = (
        df["customer_id"]
        .astype("string")
    )

    invalid_mask = (
        customer_values.notna()
        & ~customer_values.isin(
            valid_customer_ids
        )
    )

    invalid = set(
        df.index[
            invalid_mask
        ].tolist()
    )

    results.append(
        build_rule_result(
            "sales",
            "customer_reference_exists",
            evaluated_rows,
            invalid,
        )
    )

    invalid_sets.append(invalid)

    # --------------------------------------------------------
    # Rule 5 - product reference must exist
    # --------------------------------------------------------

    valid_product_ids = set(
        products["product_id"]
        .dropna()
        .astype(str)
    )

    product_values = (
        df["product_id"]
        .astype("string")
    )

    invalid_mask = (
        product_values.notna()
        & ~product_values.isin(
            valid_product_ids
        )
    )

    invalid = set(
        df.index[
            invalid_mask
        ].tolist()
    )

    results.append(
        build_rule_result(
            "sales",
            "product_reference_exists",
            evaluated_rows,
            invalid,
        )
    )

    invalid_sets.append(invalid)

    return results, invalid_sets


def validate_purchases(
    df: pd.DataFrame,
    suppliers: pd.DataFrame,
    products: pd.DataFrame,
) -> tuple[list[dict], list[set[int]]]:
    """
    Validate PURCHASES dataset.
    """

    results: list[dict] = []
    invalid_sets: list[set[int]] = []

    evaluated_rows = len(df)

    # --------------------------------------------------------
    # Rule 1 - supplier reference must exist
    # --------------------------------------------------------

    valid_supplier_ids = set(
        suppliers["supplier_id"]
        .dropna()
        .astype(str)
    )

    supplier_values = (
        df["supplier_id"]
        .astype("string")
    )

    invalid_mask = (
        supplier_values.notna()
        & ~supplier_values.isin(
            valid_supplier_ids
        )
    )

    invalid = set(
        df.index[
            invalid_mask
        ].tolist()
    )

    results.append(
        build_rule_result(
            "purchases",
            "supplier_reference_exists",
            evaluated_rows,
            invalid,
        )
    )

    invalid_sets.append(invalid)

    # --------------------------------------------------------
    # Rule 2 - product reference must exist
    # --------------------------------------------------------

    valid_product_ids = set(
        products["product_id"]
        .dropna()
        .astype(str)
    )

    product_values = (
        df["product_id"]
        .astype("string")
    )

    invalid_mask = (
        product_values.notna()
        & ~product_values.isin(
            valid_product_ids
        )
    )

    invalid = set(
        df.index[
            invalid_mask
        ].tolist()
    )

    results.append(
        build_rule_result(
            "purchases",
            "product_reference_exists",
            evaluated_rows,
            invalid,
        )
    )

    invalid_sets.append(invalid)

    # --------------------------------------------------------
    # Rule 3 - received_date >= order_date
    # --------------------------------------------------------

    order_dates = pd.to_datetime(
        df["order_date"],
        errors="coerce",
    )

    received_dates = pd.to_datetime(
        df["received_date"],
        errors="coerce",
    )

    invalid_mask = (
        order_dates.notna()
        & received_dates.notna()
        & (received_dates < order_dates)
    )

    invalid = set(
        df.index[
            invalid_mask
        ].tolist()
    )

    results.append(
        build_rule_result(
            "purchases",
            "received_date_valid",
            evaluated_rows,
            invalid,
        )
    )

    invalid_sets.append(invalid)

    return results, invalid_sets


# ============================================================
# MAIN VALIDATION PIPELINE
# ============================================================

def main() -> None:
    """
    Execute the complete RAW Data Quality pipeline.
    """

    logger.info(
        "Starting RAW Data Quality validation."
    )

    QUALITY_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Create database engine
    # --------------------------------------------------------

    engine = get_engine()

    # --------------------------------------------------------
    # Load RAW datasets
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

    purchases = load_table(
        engine,
        "purchases",
    )

    sales = load_table(
        engine,
        "sales",
    )

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    all_results: list[dict] = []
    summary_results: list[dict] = []

    # ========================================================
    # PRODUCTS
    # ========================================================

    product_results, product_invalid_sets = (
        validate_products(products)
    )

    all_results.extend(
        product_results
    )

    summary_results.append(
        build_summary(
            "products",
            len(products),
            product_results,
            product_invalid_sets,
        )
    )

    # ========================================================
    # SALES
    # ========================================================

    sales_results, sales_invalid_sets = (
        validate_sales(
            sales,
            products,
            customers,
        )
    )

    all_results.extend(
        sales_results
    )

    summary_results.append(
        build_summary(
            "sales",
            len(sales),
            sales_results,
            sales_invalid_sets,
        )
    )

    # ========================================================
    # PURCHASES
    # ========================================================

    purchase_results, purchase_invalid_sets = (
        validate_purchases(
            purchases,
            suppliers,
            products,
        )
    )

    all_results.extend(
        purchase_results
    )

    summary_results.append(
        build_summary(
            "purchases",
            len(purchases),
            purchase_results,
            purchase_invalid_sets,
        )
    )

    # --------------------------------------------------------
    # Save detailed report
    # --------------------------------------------------------

    report_df = pd.DataFrame(
        all_results
    )

    report_df.to_csv(
        QUALITY_REPORT_PATH,
        index=False,
    )

    # --------------------------------------------------------
    # Save summary
    # --------------------------------------------------------

    summary_df = pd.DataFrame(
        summary_results
    )

    summary_df.to_csv(
        QUALITY_SUMMARY_PATH,
        index=False,
    )

    # --------------------------------------------------------
    # Console output
    # --------------------------------------------------------

    logger.info(
        "Data Quality validation completed."
    )

    print("\n" + "=" * 80)
    print("EODIP DATA QUALITY SUMMARY")
    print("=" * 80)

    print(
        summary_df.to_string(
            index=False
        )
    )

    print("\nDetailed report:")
    print(
        QUALITY_REPORT_PATH
    )

    print("\nSummary report:")
    print(
        QUALITY_SUMMARY_PATH
    )

    print("=" * 80)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()