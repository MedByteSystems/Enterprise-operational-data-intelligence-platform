from __future__ import annotations

import random
from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# Configuration
# ============================================================

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "data" / "raw"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

N_SUPPLIERS = 80
N_PRODUCTS = 300
N_CUSTOMERS = 2_000
N_WAREHOUSES = 12
N_PURCHASES = 20_000
N_SALES = 100_000

START_DATE = pd.Timestamp("2024-01-01")
END_DATE = pd.Timestamp("2025-12-31")


# ============================================================
# Reference data
# ============================================================

COUNTRIES = [
    "Morocco",
    "Spain",
    "France",
    "Italy",
    "Turkey",
    "Egypt",
    "Portugal",
    "Netherlands",
]

CITIES = [
    "Casablanca",
    "Rabat",
    "Marrakesh",
    "Tangier",
    "Agadir",
    "Fes",
    "Barcelona",
    "Madrid",
    "Valencia",
    "Paris",
    "Milan",
    "Istanbul",
]

PRODUCT_CATEGORIES = [
    "Fruits",
    "Vegetables",
    "Grains",
    "Seeds",
    "Oils",
    "Legumes",
]

PRODUCT_NAMES = [
    "Tomatoes",
    "Potatoes",
    "Onions",
    "Oranges",
    "Apples",
    "Bananas",
    "Olives",
    "Almonds",
    "Chickpeas",
    "Lentils",
    "Sunflower Seeds",
    "Wheat",
    "Barley",
    "Corn",
    "Olive Oil",
    "Sunflower Oil",
]

CUSTOMER_SEGMENTS = [
    "Wholesale",
    "Retail",
    "Distributor",
    "Restaurant",
]


# ============================================================
# Helper functions
# ============================================================

def random_dates(size: int) -> pd.DatetimeIndex:
    days = (END_DATE - START_DATE).days
    offsets = np.random.randint(0, days + 1, size=size)
    return START_DATE + pd.to_timedelta(offsets, unit="D")


def random_string(prefix: str, number: int) -> str:
    return f"{prefix}_{number:05d}"


# ============================================================
# Suppliers
# ============================================================

def generate_suppliers() -> pd.DataFrame:
    rows = []

    for i in range(1, N_SUPPLIERS + 1):
        country = random.choice(COUNTRIES)

        rows.append(
            {
                "supplier_id": f"SUP{i:04d}",
                "supplier_name": f"Supplier Company {i:03d}",
                "country": country,
                "city": random.choice(CITIES),
                "status": random.choice(["Active", "Active", "Active", "Inactive"]),
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# Products
# ============================================================

def generate_products() -> pd.DataFrame:
    rows = []

    for i in range(1, N_PRODUCTS + 1):
        category = random.choice(PRODUCT_CATEGORIES)
        base_cost = round(random.uniform(2, 80), 2)
        selling_price = round(base_cost * random.uniform(1.15, 1.60), 2)

        rows.append(
            {
                "product_id": f"PROD{i:05d}",
                "product_name": f"{random.choice(PRODUCT_NAMES)} {i:03d}",
                "category": category,
                "unit_cost": base_cost,
                "unit_price": selling_price,
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# Customers
# ============================================================

def generate_customers() -> pd.DataFrame:
    rows = []

    for i in range(1, N_CUSTOMERS + 1):
        rows.append(
            {
                "customer_id": f"CUST{i:05d}",
                "customer_name": f"Customer {i:05d}",
                "country": random.choice(["Morocco", "France", "Spain", "Portugal"]),
                "city": random.choice(CITIES),
                "customer_segment": random.choice(CUSTOMER_SEGMENTS),
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# Warehouses
# ============================================================

def generate_warehouses() -> pd.DataFrame:
    rows = []

    for i in range(1, N_WAREHOUSES + 1):
        rows.append(
            {
                "warehouse_id": f"WH{i:03d}",
                "warehouse_name": f"Warehouse {i:02d}",
                "city": random.choice(CITIES),
                "country": "Morocco",
                "capacity": random.randint(5_000, 50_000),
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# Purchases
# ============================================================

def generate_purchases(
    suppliers: pd.DataFrame,
    products: pd.DataFrame,
    warehouses: pd.DataFrame,
) -> pd.DataFrame:

    supplier_ids = suppliers["supplier_id"].tolist()
    product_ids = products["product_id"].tolist()
    warehouse_ids = warehouses["warehouse_id"].tolist()

    dates = random_dates(N_PURCHASES)

    rows = []

    for i in range(1, N_PURCHASES + 1):
        order_date = dates[i - 1]

        expected_date = order_date + pd.Timedelta(
            days=random.randint(5, 30)
        )

        received_date = expected_date + pd.Timedelta(
            days=random.randint(-3, 15)
        )

        product = products.sample(1).iloc[0]

        rows.append(
            {
                "purchase_id": f"PO{i:06d}",
                "supplier_id": random.choice(supplier_ids),
                "product_id": random.choice(product_ids),
                "warehouse_id": random.choice(warehouse_ids),
                "order_date": order_date,
                "expected_date": expected_date,
                "received_date": received_date,
                "quantity": random.randint(10, 5_000),
                "unit_cost": product["unit_cost"],
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# Sales
# ============================================================

def generate_sales(
    customers: pd.DataFrame,
    products: pd.DataFrame,
    warehouses: pd.DataFrame,
) -> pd.DataFrame:

    customer_ids = customers["customer_id"].tolist()
    product_ids = products["product_id"].tolist()
    warehouse_ids = warehouses["warehouse_id"].tolist()

    dates = random_dates(N_SALES)

    rows = []

    for i in range(1, N_SALES + 1):
        product = products.sample(1).iloc[0]

        rows.append(
            {
                "sale_id": f"SALE{i:07d}",
                "customer_id": random.choice(customer_ids),
                "product_id": product["product_id"],
                "warehouse_id": random.choice(warehouse_ids),
                "sale_date": dates[i - 1],
                "quantity": random.randint(1, 500),
                "unit_price": product["unit_price"],
                "discount": round(random.uniform(0, 0.15), 3),
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# Inject data quality issues
# ============================================================

def inject_quality_issues(
    suppliers: pd.DataFrame,
    products: pd.DataFrame,
    customers: pd.DataFrame,
    warehouses: pd.DataFrame,
    purchases: pd.DataFrame,
    sales: pd.DataFrame,
) -> tuple[pd.DataFrame, ...]:

    # ------------------------------
    # Sales: missing values
    # ------------------------------
    sales.loc[100:109, "customer_id"] = np.nan

    # ------------------------------
    # Sales: invalid quantities
    # ------------------------------
    sales.loc[200:204, "quantity"] = -10

    # ------------------------------
    # Sales: duplicate records
    # ------------------------------
    sales = pd.concat(
        [sales, sales.iloc[300:310]],
        ignore_index=True,
    )

    # ------------------------------
    # Purchases: invalid dates
    # ------------------------------
    purchases.loc[50:54, "received_date"] = (
        purchases.loc[50:54, "order_date"] - pd.Timedelta(days=10)
    )

    # ------------------------------
    # Products: missing category
    # ------------------------------
    products.loc[10:14, "category"] = np.nan

    # ------------------------------
    # Purchases: invalid supplier references
    # ------------------------------
    purchases.loc[100:104, "supplier_id"] = "SUP9999"

    return (
        suppliers,
        products,
        customers,
        warehouses,
        purchases,
        sales,
    )


# ============================================================
# Main
# ============================================================

def main() -> None:
    print("Generating synthetic operational data...")

    suppliers = generate_suppliers()
    products = generate_products()
    customers = generate_customers()
    warehouses = generate_warehouses()

    purchases = generate_purchases(
        suppliers,
        products,
        warehouses,
    )

    sales = generate_sales(
        customers,
        products,
        warehouses,
    )

    (
        suppliers,
        products,
        customers,
        warehouses,
        purchases,
        sales,
    ) = inject_quality_issues(
        suppliers,
        products,
        customers,
        warehouses,
        purchases,
        sales,
    )

    datasets = {
        "suppliers.csv": suppliers,
        "products.csv": products,
        "customers.csv": customers,
        "warehouses.csv": warehouses,
        "purchases.csv": purchases,
        "sales.csv": sales,
    }

    for filename, dataframe in datasets.items():
        path = OUTPUT_DIR / filename
        dataframe.to_csv(path, index=False)

        print(
            f"Created {filename}: "
            f"{len(dataframe):,} rows"
        )

    print()
    print(f"Data generated successfully in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()