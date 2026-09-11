# EODIP — Enterprise Operational Data Intelligence Platform

**End-to-End Data Engineering Platform for Supply Chain, Inventory, Procurement, Sales & Decision Intelligence**

EODIP is an end-to-end Data Engineering and Business Intelligence platform designed to transform raw operational data into reliable analytical datasets and decision-ready dashboards.

The platform implements a complete data pipeline covering ingestion, data cleaning, staging, dimensional modeling, data warehousing, BI views, automated data quality validation, and Power BI reporting.

> **Project type:** Data Engineering / BI
> **Context:** Supply Chain, Sales, Procurement & Operational Analytics
> **Status:** End-to-end pipeline operational

---

## 1. Objectives

EODIP aims to provide a structured analytical platform capable of:

* ingesting operational data;
* cleaning and standardizing raw datasets;
* preparing reliable staging tables;
* building a dimensional Data Warehouse;
* providing analytical BI views;
* validating data quality automatically;
* exposing business KPIs through Power BI;
* enabling reproducible end-to-end pipeline execution.

---

## 2. Architecture

```text
                    OPERATIONAL DATA SOURCES
                              │
                              ▼
                     ┌─────────────────┐
                     │      RAW        │
                     │ Raw operational │
                     │      data       │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │    STAGING      │
                     │ Cleaning /      │
                     │ Transformation  │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │      DWH        │
                     │ Star Schema     │
                     │ Dimensions      │
                     │ Facts           │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │       BI        │
                     │ Analytical      │
                     │ Views           │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │    QUALITY      │
                     │   Validation    │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │    Power BI     │
                     │ Decision        │
                     │ Dashboard       │
                     └─────────────────┘
```

---

## 3. Data Pipeline

The complete pipeline is executed through a single entry point:

```bash
python run_pipeline.py
```

Execution flow:

```text
RAW ingestion
      ↓
RAW → STAGING
      ↓
STAGING → DWH
      ↓
DWH → BI
      ↓
Data Quality Validation
```

A successful execution ends with:

```text
EODIP PIPELINE COMPLETED SUCCESSFULLY
```

---

## 4. Data Layers

### RAW

Contains the original operational datasets before analytical transformation.

Current source entities:

* customers
* products
* suppliers
* warehouses
* sales
* purchases

### STAGING

Contains cleaned and standardized operational data.

Current validated row counts:

| Table              |   Rows |
| ------------------ | -----: |
| staging.customers  |  2,000 |
| staging.products   |    295 |
| staging.suppliers  |     80 |
| staging.warehouses |     12 |
| staging.sales      | 98,315 |
| staging.purchases  | 19,646 |

### Data Warehouse

The warehouse follows a **star schema**.

#### Dimensions

```text
dim_date
dim_product
dim_customer
dim_supplier
dim_warehouse
```

#### Fact tables

```text
fact_sales
fact_purchases
```

Current warehouse row counts:

| Table          |   Rows |
| -------------- | -----: |
| dim_date       |    771 |
| dim_product    |    295 |
| dim_customer   |  2,000 |
| dim_supplier   |     80 |
| dim_warehouse  |     12 |
| fact_sales     | 98,315 |
| fact_purchases | 19,646 |

---

## 5. BI Layer

The analytical layer is implemented through PostgreSQL views in the `bi` schema.

```text
bi.vw_sales_performance
bi.vw_purchase_performance
bi.vw_supply_chain_performance
```

These views combine fact and dimension data to provide business-ready analytical datasets for reporting.

### Main analytical areas

**Sales**

* sales evolution
* sales by category
* top products
* units sold
* sales count
* total sales

**Procurement**

* total purchases
* purchase count
* purchase amounts
* supplier performance

**Supply Chain**

* delivery delay
* late delivery rate
* supplier delivery performance
* purchase delivery status

---

## 6. Power BI Dashboard

The BI layer feeds a Power BI dashboard focused on **Sales & Supply Chain Performance**.

Main KPIs include:

* Total Sales
* Total Purchases
* Units Sold
* Sales Count
* Purchase Count
* Late Delivery Rate
* Average Delivery Delay

Main visuals include:

* Sales vs Purchases Evolution
* Sales by Category
* Top 10 Products by Sales
* Top 10 Suppliers by Average Delivery Delay
* Purchase Delivery Status
* Date filtering
* Category filtering

---

## 7. Data Quality

EODIP includes automated validation after the DWH and BI layers.

The validation checks:

### Table availability

Ensures that required RAW, STAGING and DWH tables exist and contain data.

### Referential integrity

Validates relationships between fact tables and dimensions, including:

* sales → date
* sales → product
* sales → customer
* sales → warehouse
* purchases → date
* purchases → product
* purchases → supplier
* purchases → warehouse

### Critical NULL checks

Validates important foreign keys such as:

```text
fact_sales.date_key
fact_sales.product_key
fact_purchases.date_key
fact_purchases.product_key
```

### BI validation

Ensures that the analytical BI views are available.

Validation script:

```bash
python src/validation/validate_pipeline.py
```

---

## 8. Technology Stack

| Layer           | Technology                 |
| --------------- | -------------------------- |
| Programming     | Python                     |
| Data Processing | Pandas / NumPy             |
| Database        | PostgreSQL                 |
| SQL             | PostgreSQL SQL             |
| Data Warehouse  | Star Schema                |
| BI              | Power BI                   |
| Database Access | SQLAlchemy / Psycopg       |
| Environment     | Python virtual environment |
| Version Control | Git / GitHub               |

---

## 9. Project Structure

```text
enterprise-operational-data-intelligence-platform/
│
├── data/
│
├── docker/
│
├── docs/
│   ├── architecture/
│   └── business/
│
├── notebooks/
│
├── powerbi/
│
├── sql/
│   └── bi/
│       ├── vw_sales_performance.sql
│       ├── vw_purchase_performance.sql
│       └── vw_supply_chain_performance.sql
│
├── src/
│   ├── data_generation/
│   ├── ingestion/
│   ├── quality/
│   ├── transformation/
│   ├── warehouse/
│   ├── bi/
│   └── validation/
│
├── tests/
│
├── .env.example
├── requirements.txt
└── run_pipeline.py
```

---

## 10. Configuration

Create a local `.env` file from `.env.example`.

Example:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
```

> `.env` is intentionally excluded from version control.

---

## 11. Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows / Git Bash:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure `.env` and ensure PostgreSQL is running.

---

## 12. Run the Full Pipeline

Execute:

```bash
python run_pipeline.py
```

The pipeline performs:

```text
1. RAW ingestion
2. RAW → STAGING transformation
3. STAGING → DWH loading
4. DWH → BI view creation
5. Automated data quality validation
```

---

## 13. Validation

The data quality layer can also be executed independently:

```bash
python src/validation/validate_pipeline.py
```

Expected final result:

```text
EODIP VALIDATION COMPLETED SUCCESSFULLY
```

---

## 14. Business Value

EODIP transforms operational data into decision-ready information for supply chain and management teams.

The platform enables analysis of:

* sales performance;
* procurement activity;
* supplier delivery performance;
* delivery delays;
* product performance;
* category performance;
* operational trends.

The architecture separates operational processing from analytical consumption, improving reliability and maintainability.

---

## 15. Current Scope

The current implementation focuses on:

```text
Data ingestion
→ Data preparation
→ Dimensional warehouse
→ BI layer
→ Data quality
→ Decision dashboard
```

Inventory analytics are not currently implemented as a dedicated fact table because the current source dataset does not contain an explicit inventory or stock-movement source.

---

## 16. Future Improvements

Possible production-oriented extensions include:

* workflow orchestration with Airflow, Prefect or Dagster;
* scheduled pipeline execution;
* incremental data loading;
* centralized monitoring and alerting;
* Dockerized deployment;
* CI/CD;
* cloud data warehouse deployment;
* advanced predictive analytics and machine learning.

---

## 17. Project Outcome

EODIP provides a reproducible end-to-end Data Engineering pipeline transforming raw operational datasets into validated analytical data and Power BI decision dashboards.

The project demonstrates practical skills in:

**Python · SQL · PostgreSQL · ETL · Data Quality · Data Warehousing · Dimensional Modeling · BI · Power BI · Git**
