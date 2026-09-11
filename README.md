# EODIP — Enterprise Operational Data Intelligence Platform

**End-to-End Data Engineering Platform for Supply Chain, Inventory, Procurement, Sales & Decision Intelligence**

EODIP is an end-to-end Data Engineering and Business Intelligence platform designed to transform raw operational data into reliable analytical datasets and decision-ready dashboards.

The platform implements a complete data pipeline covering data ingestion, cleaning, staging, dimensional modeling, data warehousing, BI views, automated data quality validation, Dockerized PostgreSQL, and Power BI reporting.

> **Project type:** Data Engineering / Business Intelligence
> **Domain:** Supply Chain, Sales, Procurement & Operational Analytics
> **Status:** End-to-end pipeline operational

---

## 1. Objectives

EODIP aims to provide a structured analytical platform capable of:

* ingesting operational data;
* cleaning and standardizing raw datasets;
* preparing reliable staging data;
* building a dimensional Data Warehouse;
* providing business-oriented BI views;
* validating data quality automatically;
* exposing operational KPIs through Power BI;
* running the complete pipeline reproducibly;
* providing a containerized PostgreSQL environment with Docker.

---

## 2. Architecture

```text
                         OPERATIONAL DATA
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Docker PostgreSQL │
                    │      localhost      │
                    │       :5433         │
                    └──────────┬──────────┘
                               │
                               ▼
                         ┌───────────┐
                         │    RAW    │
                         │ Raw data  │
                         └─────┬─────┘
                               │
                               ▼
                       ┌──────────────┐
                       │   STAGING    │
                       │ Cleaning &   │
                       │ Transformation
                       └──────┬───────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │       DWH       │
                     │   Star Schema  │
                     │ Dimensions/Facts
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │       BI        │
                     │ PostgreSQL Views│
                     └────────┬────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Automated Data Quality │
                  │      Validation         │
                  └───────────┬────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │     Power BI    │
                     │ Decision        │
                     │ Dashboard       │
                     └─────────────────┘
```

### Logical data flow

```text
RAW
 ↓
STAGING
 ↓
DATA WAREHOUSE
 ↓
BI VIEWS
 ↓
DATA QUALITY VALIDATION
 ↓
POWER BI
```

---

## 3. End-to-End Pipeline

The complete pipeline is orchestrated through a single Python entry point:

```bash
python run_pipeline.py
```

Execution flow:

```text
1. RAW ingestion
        ↓
2. RAW → STAGING
        ↓
3. STAGING → DWH
        ↓
4. DWH → BI
        ↓
5. Data Quality Validation
```

Successful execution ends with:

```text
EODIP PIPELINE COMPLETED SUCCESSFULLY
```

---

## 4. Data Layers

### RAW

The RAW layer contains the original operational datasets before analytical transformation.

Current source entities:

```text
customers
products
suppliers
warehouses
sales
purchases
```

Current RAW volumes:

| Table          |    Rows |
| -------------- | ------: |
| raw.customers  |   2,000 |
| raw.products   |     300 |
| raw.suppliers  |      80 |
| raw.warehouses |      12 |
| raw.sales      | 100,010 |
| raw.purchases  |  20,000 |

---

### STAGING

The STAGING layer contains cleaned and standardized operational data.

Current STAGING volumes:

| Table              |   Rows |
| ------------------ | -----: |
| staging.customers  |  2,000 |
| staging.products   |    295 |
| staging.suppliers  |     80 |
| staging.warehouses |     12 |
| staging.sales      | 98,315 |
| staging.purchases  | 19,646 |

The reduction in row counts reflects the data cleaning and validation rules applied during transformation.

---

## 5. Data Warehouse

The analytical warehouse follows a **star schema**.

### Dimensions

```text
dim_date
dim_product
dim_customer
dim_supplier
dim_warehouse
```

### Fact tables

```text
fact_sales
fact_purchases
```

Current DWH volumes:

| Table              |   Rows |
| ------------------ | -----: |
| dwh.dim_date       |    771 |
| dwh.dim_product    |    295 |
| dwh.dim_customer   |  2,000 |
| dwh.dim_supplier   |     80 |
| dwh.dim_warehouse  |     12 |
| dwh.fact_sales     | 98,315 |
| dwh.fact_purchases | 19,646 |

### Analytical model

```text
                 dim_date
                    │
                    │
dim_product ─── fact_sales ─── dim_customer
                    │
                    │
              dim_warehouse


                 dim_date
                    │
                    │
dim_product ─ fact_purchases ─ dim_supplier
                    │
                    │
              dim_warehouse
```

---

## 6. BI Layer

The BI layer provides business-ready analytical views in the PostgreSQL `bi` schema.

```text
bi.vw_sales_performance
bi.vw_purchase_performance
bi.vw_supply_chain_performance
```

These views combine fact and dimension data for reporting and analytical consumption.

### Sales analytics

The BI layer supports:

* total sales;
* sales evolution;
* sales by category;
* top products;
* units sold;
* sales count.

### Procurement analytics

The BI layer supports:

* total purchases;
* purchase count;
* purchase amounts;
* supplier performance.

### Supply Chain analytics

The BI layer supports:

* average delivery delay;
* late delivery rate;
* supplier delivery performance;
* purchase delivery status;
* operational performance by warehouse and product.

---

## 7. Power BI Dashboard

Power BI consumes the `bi` views from the PostgreSQL Docker environment.

Connection:

```text
Server: localhost:5433
Database: postgres
Schema: bi
```

The dashboard is focused on **Sales & Supply Chain Performance**.

### KPI cards

* Total Sales
* Total Purchases
* Units Sold
* Sales Count
* Purchase Count
* Late Delivery Rate
* Average Delivery Delay

### Main visuals

* Sales vs Purchases Evolution
* Sales by Category
* Top 10 Products by Sales
* Top 10 Suppliers by Average Delivery Delay
* Purchase Delivery Status

### Interactive filters

* Date
* Category

The dashboard provides a decision-oriented view of sales, procurement and supply chain performance.

---

## 8. Data Quality

EODIP includes an automated validation layer executed after the BI layer.

The validation script is:

```bash
python src/validation/validate_pipeline.py
```

### Checks performed

#### Table availability

Ensures required RAW, STAGING and DWH tables exist and contain data.

#### Referential integrity

Checks fact-to-dimension relationships:

```text
Sales → Date
Sales → Product
Sales → Customer
Sales → Warehouse

Purchases → Date
Purchases → Product
Purchases → Supplier
Purchases → Warehouse
```

#### Critical NULL checks

Checks important foreign keys such as:

```text
fact_sales.date_key
fact_sales.product_key
fact_purchases.date_key
fact_purchases.product_key
```

#### BI checks

Ensures the three analytical BI views exist and contain data:

```text
bi.vw_sales_performance
bi.vw_purchase_performance
bi.vw_supply_chain_performance
```

Successful validation ends with:

```text
EODIP VALIDATION COMPLETED SUCCESSFULLY
```

---

## 9. Docker

PostgreSQL is containerized with Docker Compose.

### Start the database

```bash
docker compose up -d
```

### Check the container

```bash
docker ps
```

The PostgreSQL container is exposed on:

```text
localhost:5433
```

while PostgreSQL inside the container listens on its standard port:

```text
5432
```

This avoids conflicts with the local PostgreSQL installation on Windows.

### Stop the database

```bash
docker compose down
```

### Database persistence

Docker Compose uses a named volume:

```text
eodip_postgres_data
```

to persist PostgreSQL data across container restarts.

---

## 10. Technology Stack

| Layer            | Technology                 |
| ---------------- | -------------------------- |
| Programming      | Python                     |
| Data Processing  | Pandas / NumPy             |
| Database         | PostgreSQL                 |
| SQL              | PostgreSQL SQL             |
| Data Warehouse   | Star Schema                |
| BI               | Power BI                   |
| Database Access  | Psycopg / SQLAlchemy       |
| Containerization | Docker / Docker Compose    |
| Environment      | Python Virtual Environment |
| Version Control  | Git / GitHub               |

---

## 11. Project Structure

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
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── run_pipeline.py
└── README.md
```

---

## 12. Configuration

Create a local `.env` file from `.env.example`.

For the Docker environment:

```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
```

> `.env` contains local configuration and is intentionally excluded from Git version control.

---

## 13. Installation

### 1. Clone the repository

```bash
git clone https://github.com/MedByteSystems/enterprise-operational-data-intelligence-platform.git
cd enterprise-operational-data-intelligence-platform
```

### 2. Create the Python virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Git Bash:

```bash
source .venv/Scripts/activate
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 5. Start PostgreSQL with Docker

```bash
docker compose up -d
```

### 6. Configure environment variables

Create `.env` from `.env.example`.

Use:

```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
```

---

## 14. Run the Complete Platform

Once Docker and the Python environment are ready:

```bash
python run_pipeline.py
```

The command executes:

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

Expected result:

```text
EODIP PIPELINE COMPLETED SUCCESSFULLY
```

---

## 15. Run Data Quality Validation Independently

The validation layer can also be executed independently:

```bash
python src/validation/validate_pipeline.py
```

Expected result:

```text
EODIP VALIDATION COMPLETED SUCCESSFULLY
```

---

## 16. Business Value

EODIP transforms operational data into decision-ready information for management, procurement, sales and supply chain analysis.

The platform supports questions such as:

### Sales

* Which products generate the highest sales?
* Which categories perform best?
* How do sales evolve over time?

### Procurement

* How much is being purchased?
* Which suppliers contribute the most purchasing volume?
* How does purchasing evolve over time?

### Supply Chain

* Which suppliers have the longest delivery delays?
* What percentage of purchases are late?
* How does delivery performance evolve over time?

### Management

* What are the main sales and procurement trends?
* Which operational indicators require attention?

---

## 17. Current Scope and Limitation

The current implementation includes sales, procurement, supplier, warehouse and product analytics.

A dedicated `fact_inventory` table is **not implemented** because the current operational source data does not provide an explicit inventory or stock-movement dataset.

Therefore, inventory metrics are not artificially generated.

This keeps the analytical model aligned with the available business data.

---

## 18. Reproducibility

The project is designed to be reproducible through:

```text
Docker PostgreSQL
        +
Python virtual environment
        +
Environment configuration
        +
Single pipeline entry point
        +
Automated data quality validation
```

Main execution command:

```bash
docker compose up -d
python run_pipeline.py
```

This provides a reproducible local execution environment for the complete EODIP data pipeline.

---

## 19. Future Improvements

Potential production-oriented extensions include:

* workflow orchestration with Airflow, Prefect or Dagster;
* scheduled pipeline execution;
* incremental data loading;
* centralized monitoring and alerting;
* CI/CD;
* cloud deployment;
* cloud data warehouse integration;
* advanced predictive analytics;
* machine learning use cases.

These extensions are outside the current MVP scope.

---

## 20. Project Outcome

EODIP provides a complete end-to-end Data Engineering and Business Intelligence platform transforming raw operational data into validated analytical datasets and decision-ready dashboards.

The project demonstrates practical capabilities in:

**Python · SQL · PostgreSQL · Docker · ETL · Data Quality · Data Warehousing · Dimensional Modeling · BI · Power BI · Git/GitHub**

The platform can be executed end-to-end through:

```bash
docker compose up -d
python run_pipeline.py
```

with automated validation confirming the integrity of the resulting analytical data.
