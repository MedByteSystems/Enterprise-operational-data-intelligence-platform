# Software Architecture Document

## Enterprise Operational Data Intelligence Platform (EODIP)

**Version:** 1.0
**Status:** Architecture Baseline
**Author:** Data analytics team 
**Domain:** Data Engineering / Business Intelligence / Artificial Intelligence
**Target Environment:** Local development with Dockerized services
**Project Duration:** Approximately 8 weeks / 160 hours

---

# 1. Introduction

## 1.1 Purpose

The purpose of this document is to define the software architecture of the Enterprise Operational Data Intelligence Platform (EODIP).

This document establishes the architectural foundation required to design and implement an enterprise-oriented data platform capable of collecting, validating, transforming, storing, analyzing, and exposing operational data.

It serves as the main technical reference for the project and will guide implementation, testing, deployment, and documentation activities.

The architecture is designed to demonstrate the complete data value chain expected from a modern Data Engineering solution, from raw data acquisition to business intelligence, machine learning, and API consumption.

---

## 1.2 Document Scope

This document defines:

* Business context and project objectives.
* Functional and non-functional requirements.
* System architecture.
* Data architecture.
* Data ingestion strategy.
* Data quality strategy.
* ETL/ELT processing.
* Data warehouse design.
* Business intelligence layer.
* Machine learning layer.
* API layer.
* Deployment architecture.
* Technology choices.
* Development roadmap.
* Architectural decisions and constraints.

The document does not define detailed implementation code. Implementation specifications will be documented separately when required.

---

## 1.3 Intended Audience

This document is intended for:

* Data Engineers.
* BI Engineers and Data Analysts.
* Software Engineers.
* Technical reviewers.
* Project supervisors.
* Recruiters and technical interviewers.
* Future contributors to the platform.

---

# 2. Project Overview

## 2.1 Vision

The vision of EODIP is to build an enterprise-oriented data platform capable of transforming operational data into reliable and actionable business intelligence.

The platform provides a unified data ecosystem where information from multiple operational processes can be acquired, validated, transformed, centralized, analyzed, and exposed to business applications.

The platform demonstrates how an organization can move from fragmented operational data to trusted analytical and predictive capabilities.

---

## 2.2 Business Context

The initial business context is inspired by an agricultural supply chain and international trade environment.

The modeled business ecosystem includes:

* Suppliers.
* Procurement.
* Import operations.
* Logistics and transportation.
* Warehouses.
* Inventory.
* Sales.
* Customers.
* Business performance.

The platform is not designed exclusively for agricultural companies.

The underlying architecture is intentionally generic so that the same data engineering principles can be applied to:

* Retail.
* Distribution.
* Manufacturing.
* Logistics.
* Financial services.
* Other organizations with operational data.

---

## 2.3 Problem Statement

Organizations frequently generate operational data through multiple business processes and systems.

However, this data may be:

* Distributed across different sources.
* Stored in inconsistent formats.
* Affected by quality issues.
* Difficult to integrate.
* Difficult to analyze historically.
* Used through manual reporting processes.

As a consequence, decision-makers may lack a reliable and centralized view of operational performance.

EODIP addresses this problem by creating a structured data platform that centralizes operational information and transforms it into trusted analytical assets.

---

## 2.4 Objectives

### 2.4.1 Data Engineering Objectives

The platform must:

* Acquire data from heterogeneous sources.
* Implement reproducible ingestion processes.
* Validate incoming data.
* Detect and document data quality issues.
* Transform operational data into analytical structures.
* Store curated data in a centralized warehouse.
* Provide traceability between raw and transformed data.

### 2.4.2 Business Intelligence Objectives

The platform must:

* Provide reliable business KPIs.
* Support historical analysis.
* Provide interactive dashboards.
* Enable analysis of procurement, inventory, sales, suppliers, customers, and logistics.
* Support operational decision-making.

### 2.4.3 Artificial Intelligence Objectives

The platform must demonstrate:

* Preparation of analytical datasets for machine learning.
* Feature engineering.
* Training and evaluation of predictive models.
* Integration of predictions into the data platform.
* Business interpretation of model outputs.

### 2.4.4 Software Engineering Objectives

The platform must:

* Follow a modular architecture.
* Use Git for version control.
* Provide automated or reproducible workflows.
* Expose selected data capabilities through REST APIs.
* Use Docker for reproducible execution environments.
* Include automated tests.
* Provide technical documentation.

---

# 3. Functional Requirements

## 3.1 Business Processes

The platform models the following operational flow:

```text
Suppliers
    ↓
Procurement
    ↓
Import / Logistics
    ↓
Warehouses
    ↓
Inventory
    ↓
Sales
    ↓
Customers
    ↓
Business Intelligence
    ↓
Predictive Analytics
    ↓
Decision Support
```

---

## 3.2 Functional Capabilities

### FR-01 — Data Source Management

The platform shall support the ingestion of structured operational data originating from sources such as:

* CSV files.
* Excel files where applicable.
* Relational databases.
* Generated operational datasets.

The initial implementation will prioritize CSV and PostgreSQL sources.

---

### FR-02 — Data Ingestion

The platform shall provide reproducible ingestion pipelines capable of:

* Reading source data.
* Validating file structure.
* Loading raw data.
* Recording ingestion metadata.
* Handling invalid records.
* Reporting ingestion failures.

---

### FR-03 — Data Quality

The platform shall implement data quality checks covering:

* Null values.
* Duplicate records.
* Invalid dates.
* Invalid numerical values.
* Referential integrity.
* Domain constraints.
* Unexpected categories.
* Schema inconsistencies.

Data quality results shall be measurable and traceable.

---

### FR-04 — Data Transformation

The platform shall transform raw operational data into standardized datasets.

Transformation operations may include:

* Type normalization.
* Deduplication.
* Standardization.
* Business rule application.
* Derived attributes.
* Aggregations.
* Dimension preparation.
* Fact preparation.

---

### FR-05 — Data Warehouse

The platform shall provide a dimensional data warehouse based on a Star Schema.

The warehouse shall support analytical queries across:

* Procurement.
* Sales.
* Inventory.
* Logistics.
* Suppliers.
* Customers.
* Products.
* Time.

---

### FR-06 — Business Intelligence

The platform shall provide Power BI dashboards containing:

* Executive KPIs.
* Sales analysis.
* Inventory analysis.
* Procurement analysis.
* Supplier performance.
* Customer analysis.
* Operational trends.

---

### FR-07 — Machine Learning

The platform shall provide at least one business-relevant predictive use case.

The initial target use case is demand forecasting / sales forecasting.

The machine learning workflow shall include:

```text
Historical Data
      ↓
Feature Engineering
      ↓
Train / Validation Split
      ↓
Model Training
      ↓
Evaluation
      ↓
Prediction
      ↓
Business Consumption
```

---

### FR-08 — API

The platform shall expose selected analytical capabilities through a REST API.

The API shall provide access to:

* KPI summaries.
* Selected analytical datasets.
* Prediction results.
* Data quality indicators.

The API shall be implemented using FastAPI.

---

### FR-09 — Monitoring and Traceability

The platform shall record relevant execution information, including:

* Pipeline execution status.
* Number of records processed.
* Number of rejected records.
* Data quality results.
* Execution timestamps.
* Errors.

---

# 4. Non-Functional Requirements

## 4.1 Maintainability

The platform shall use modular components with clear responsibilities.

Business logic, data processing, API logic, and configuration shall remain separated.

---

## 4.2 Reproducibility

The project shall provide reproducible execution through:

* Git.
* Python dependency management.
* Docker.
* Configuration files.
* Documented setup procedures.

---

## 4.3 Data Quality

Data quality shall be treated as a first-class engineering concern rather than a final validation step.

---

## 4.4 Scalability

The architecture shall allow future migration from local processing toward distributed processing technologies such as PySpark and cloud data platforms.

Distributed technologies will only be introduced if justified by project requirements or available development time.

---

## 4.5 Security

The platform shall avoid storing secrets directly in source code.

Sensitive configuration such as database credentials shall be handled through environment variables.

---

## 4.6 Performance

The platform shall prioritize efficient SQL queries, appropriate indexing, and efficient batch processing.

The initial target is analytical workloads on a local PostgreSQL environment.

---

## 4.7 Testability

Critical data transformations, data quality rules, and API endpoints shall be covered by automated tests where practical.

---

# 5. Architecture Principles

The architecture follows the following principles.

## 5.1 Data First

Data quality, consistency, lineage, and accessibility are primary architectural concerns.

---

## 5.2 Separation of Concerns

Each component shall have a clearly defined responsibility.

---

## 5.3 Reproducibility

A new developer should be able to reproduce the environment and execute the platform using documented procedures.

---

## 5.4 Business Alignment

Technical components must support identifiable business requirements.

Technology shall not be introduced solely for demonstration purposes.

---

## 5.5 Quality Over Technology Count

The project prioritizes depth and engineering quality over the number of technologies used.

---

## 5.6 Incremental Architecture

The architecture shall support future extensions without requiring a complete redesign.

---

# 6. High-Level System Architecture

The target architecture is:

```text
                    OPERATIONAL DATA SOURCES
                              |
              +---------------+---------------+
              |               |               |
             CSV           PostgreSQL      Other Sources
              |               |               |
              +---------------+---------------+
                              |
                              v
                     DATA INGESTION LAYER
                              |
                              v
                         RAW DATA LAYER
                              |
                              v
                      DATA QUALITY LAYER
                              |
                              v
                    TRANSFORMATION / ELT
                              |
                              v
                    DATA WAREHOUSE
                    PostgreSQL
                              |
              +---------------+---------------+
              |                               |
              v                               v
        BUSINESS INTELLIGENCE          ML / ANALYTICS
           Power BI                         |
              |                             |
              |                             v
              |                       Predictions
              |                             |
              +---------------+-------------+
                              |
                              v
                          FASTAPI
                              |
                              v
                     DATA CONSUMERS
```

---

# 7. Data Architecture

## 7.1 Data Layers

The platform follows a layered data architecture.

### Raw Layer

Contains data as received from source systems.

Characteristics:

* Minimal transformation.
* Source preservation.
* Ingestion metadata.
* Traceability.

---

### Staging Layer

Contains standardized and validated intermediate datasets.

Typical operations include:

* Type conversion.
* Normalization.
* Deduplication.
* Basic validation.

---

### Warehouse Layer

Contains curated analytical data modeled using dimensional modeling.

---

### Analytics Layer

Contains datasets prepared for:

* BI.
* Machine learning.
* API consumption.

---

# 8. Data Warehouse Architecture

## 8.1 Dimensional Modeling

The warehouse shall primarily use a Star Schema.

The central fact tables will represent measurable business processes.

Potential fact tables include:

```text
fact_sales
fact_purchases
fact_inventory
fact_shipments
```

Dimensions may include:

```text
dim_date
dim_product
dim_supplier
dim_customer
dim_warehouse
dim_location
```

The final model will be determined during detailed data modeling.

---

## 8.2 Fact Tables

Fact tables contain measurable business events.

Examples:

### Sales

Measures may include:

* Quantity.
* Unit price.
* Revenue.
* Discount.
* Cost.
* Margin.

### Purchases

Measures may include:

* Quantity purchased.
* Purchase cost.
* Total purchase value.
* Lead time.

### Inventory

Measures may include:

* Stock quantity.
* Stock value.
* Reorder threshold.
* Inventory turnover.

---

## 8.3 Dimensions

Dimensions provide descriptive context for analytical facts.

Examples include:

* Product.
* Supplier.
* Customer.
* Warehouse.
* Date.
* Geography.

---

# 9. Data Ingestion Architecture

## 9.1 Initial Sources

The first implementation will use controlled datasets representing operational systems.

Sources will include:

* CSV datasets.
* PostgreSQL operational tables.
* Generated synthetic operational data.

Synthetic data will be designed to represent realistic business scenarios rather than arbitrary random values.

---

## 9.2 Ingestion Process

The ingestion workflow shall follow:

```text
Source
  ↓
Schema Validation
  ↓
Raw Load
  ↓
Metadata Registration
  ↓
Quality Validation
  ↓
Staging
```

---

## 9.3 Incremental Processing

Where appropriate, the platform shall support incremental ingestion based on:

* Business dates.
* Timestamps.
* Source identifiers.

Full reloads may be used for development datasets where incremental processing does not provide sufficient value.

---

# 10. Data Quality Architecture

Data quality checks shall be implemented as reusable validation rules.

## 10.1 Quality Dimensions

The platform shall evaluate:

* Completeness.
* Validity.
* Uniqueness.
* Consistency.
* Referential integrity.
* Timeliness where applicable.

---

## 10.2 Quality Reporting

Each pipeline execution should produce measurable results such as:

```text
Records processed: 10,000
Valid records:      9,850
Rejected records:     150
Quality score:       98.5%
```

The exact quality scoring methodology will be defined during implementation.

---

# 11. ETL / ELT Architecture

The project will primarily follow an ELT-oriented architecture:

```text
Extract
   ↓
Load
   ↓
Transform
   ↓
Serve
```

Python will be used for ingestion and orchestration logic where appropriate.

SQL will be used extensively for warehouse transformations and analytical logic.

Pandas will be used for controlled data preparation and processing tasks where it provides practical value.

---

# 12. Business Intelligence Architecture

Power BI will consume curated warehouse data rather than raw operational data.

The BI layer will contain several dashboards.

## 12.1 Executive Dashboard

Potential KPIs:

* Total Revenue.
* Gross Margin.
* Sales Growth.
* Inventory Value.
* Inventory Turnover.
* Purchase Value.
* Supplier Performance.

---

## 12.2 Sales Dashboard

Analysis by:

* Time.
* Product.
* Customer.
* Geography.
* Sales channel.

---

## 12.3 Inventory Dashboard

Analysis by:

* Warehouse.
* Product.
* Stock level.
* Stock movement.
* Inventory value.
* Slow-moving products.

---

## 12.4 Procurement Dashboard

Analysis by:

* Supplier.
* Product.
* Purchase value.
* Supplier lead time.
* Supplier reliability.

---

# 13. Machine Learning Architecture

## 13.1 Objective

Machine learning shall be integrated into the platform as a business capability rather than as an isolated notebook experiment.

---

## 13.2 Initial Use Case

The initial ML use case will focus on demand / sales forecasting.

The model will use historical business data to estimate future demand.

---

## 13.3 ML Pipeline

```text
Warehouse Data
      ↓
Feature Extraction
      ↓
Feature Engineering
      ↓
Dataset Creation
      ↓
Train / Validation Split
      ↓
Model Training
      ↓
Evaluation
      ↓
Prediction
      ↓
Prediction Storage
      ↓
Power BI / API
```

---

## 13.4 Model Evaluation

Models shall be evaluated using appropriate regression forecasting metrics.

Potential metrics include:

* MAE.
* RMSE.
* MAPE where appropriate.

Model selection will prioritize business usefulness and interpretability over algorithmic complexity.

---

# 14. API Architecture

FastAPI will provide a lightweight REST API over selected analytical capabilities.

Potential endpoints include:

```text
GET /health
GET /kpis
GET /sales
GET /inventory
GET /suppliers
GET /data-quality
GET /forecasts
```

The exact API contract will be defined separately in the API documentation.

---

# 15. Application Components

The platform will be organized into logical modules.

```text
src/

├── ingestion/
├── quality/
├── transformation/
├── warehouse/
├── analytics/
├── ml/
├── api/
└── common/
```

### ingestion

Responsible for source acquisition and raw loading.

### quality

Responsible for validation rules and quality reporting.

### transformation

Responsible for cleaning and business transformations.

### warehouse

Responsible for warehouse loading and database interactions.

### analytics

Responsible for KPI and analytical queries.

### ml

Responsible for feature engineering, training, evaluation, and prediction.

### api

Responsible for REST services.

### common

Contains shared configuration, utilities, logging, and common infrastructure components.

---

# 16. Technology Stack

## 16.1 Programming

### Python

Primary programming language for:

* Data ingestion.
* Data processing.
* Data quality.
* Machine learning.
* API development.

---

## 16.2 Database

### PostgreSQL 18.4

Primary relational database for:

* Operational data.
* Staging data.
* Data warehouse.
* Analytical data.

---

## 16.3 Data Processing

### Pandas

Used for controlled tabular data processing and preparation.

### NumPy

Used for numerical computation.

---

## 16.4 Machine Learning

### scikit-learn

Used for:

* Model training.
* Evaluation.
* Feature preprocessing.
* Baseline predictive models.

---

## 16.5 Business Intelligence

### Microsoft Power BI

Used for:

* KPI visualization.
* Interactive dashboards.
* Business analysis.
* Decision support.

---

## 16.6 API

### FastAPI

Used to expose selected analytical and predictive capabilities through REST APIs.

---

## 16.7 Containerization

### Docker

Used to provide reproducible development and execution environments.

---

## 16.8 Version Control

### Git

Used for source control and version history.

### GitHub

Used for repository hosting, collaboration, documentation, and project presentation.

---

# 17. Technology Expansion Strategy

Additional technologies will only be introduced when they provide measurable architectural value.

## 17.1 PySpark

PySpark may be introduced if the project requires demonstrating distributed data processing.

It shall not be added merely to increase the technology list.

---

## 17.2 Airflow

Airflow may be introduced if pipeline orchestration becomes sufficiently complex to justify a dedicated workflow orchestrator.

---

## 17.3 Cloud

Cloud deployment may be introduced after the local architecture is stable.

The local architecture shall remain fully reproducible.

---

## 17.4 GenAI

A GenAI component is explicitly considered optional.

It shall not become the central feature of the platform.

If introduced, it must solve a concrete business problem such as natural-language access to documented KPIs or analytical metadata.

---

# 18. Deployment Architecture

The initial environment will use Docker for reproducibility.

A simplified deployment architecture is:

```text
                    Docker Environment
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
   PostgreSQL        FastAPI          Data Services
        |                |                |
        +----------------+----------------+
                         |
                         v
                    Power BI
```

Python-based pipelines will run within the controlled project environment.

---

# 19. Configuration Management

Configuration shall be externalized from application code.

Environment-specific settings shall be managed through environment variables and configuration files.

Sensitive information shall not be committed to Git.

Examples include:

```text
DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
API_PORT
```

A `.env.example` file may be provided to document required configuration without exposing secrets.

---

# 20. Testing Strategy

Testing shall be implemented at multiple levels.

## 20.1 Unit Tests

Test:

* Transformation functions.
* Data validation functions.
* Feature engineering functions.
* Utility functions.

---

## 20.2 Data Quality Tests

Validate:

* Schema.
* Null constraints.
* Uniqueness.
* Referential integrity.
* Domain rules.

---

## 20.3 API Tests

Validate:

* Endpoint availability.
* Response structure.
* Error handling.
* Input validation.

---

## 20.4 Integration Tests

Validate interactions between:

* Pipelines.
* PostgreSQL.
* API.
* Warehouse.

---

# 21. Logging and Observability

The platform shall provide structured logging for important pipeline and API events.

Logs should make it possible to identify:

* Execution start.
* Execution completion.
* Records processed.
* Errors.
* Data quality failures.
* API failures.

The initial implementation will use application-level logging.

A dedicated observability stack is outside the initial scope.

---

# 22. Security Considerations

The project shall follow basic security principles.

* No credentials in source code.
* Environment variables for secrets.
* Principle of least privilege where practical.
* Separate application and database credentials where justified.
* Input validation for APIs.
* No sensitive production data in the public repository.

The datasets published with the project will be synthetic or non-sensitive.

---

# 23. Repository Architecture

The repository will follow this structure:

```text
enterprise-operational-data-intelligence-platform/

├── data/
│   ├── raw/
│   ├── staging/
│   ├── processed/
│   └── README.md
│
├── docker/
│
├── docs/
│   ├── api/
│   ├── architecture/
│   ├── business/
│   ├── decisions/
│   ├── diagrams/
│   └── data-model/
│
├── notebooks/
│
├── powerbi/
│
├── sql/
│   ├── ddl/
│   ├── staging/
│   ├── warehouse/
│   └── analytics/
│
├── src/
│   ├── ingestion/
│   ├── quality/
│   ├── transformation/
│   ├── warehouse/
│   ├── analytics/
│   ├── ml/
│   ├── api/
│   └── common/
│
├── tests/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
├── requirements.txt
└── LICENSE
```

---

# 24. Development Methodology

Development will follow an incremental approach.

Each major module shall be:

1. Designed.
2. Implemented.
3. Tested.
4. Documented.
5. Committed to Git.

Development shall prioritize functional vertical slices rather than isolated technical components.

For example:

```text
Raw Sales Data
      ↓
Ingestion
      ↓
Quality
      ↓
Warehouse
      ↓
Sales KPI
      ↓
Power BI
```

This approach ensures that business value is demonstrated throughout development.

---

# 25. Development Backlog

## Epic 1 — Project Foundation

* Repository configuration.
* Python environment.
* Dependency management.
* Configuration management.
* Docker baseline.
* Logging foundation.

---

## Epic 2 — Business and Data Modeling

* Define business processes.
* Define entities.
* Define relationships.
* Define source schemas.
* Define warehouse Star Schema.
* Create data dictionary.

---

## Epic 3 — Data Generation and Sources

* Generate realistic synthetic operational data.
* Create source datasets.
* Define data anomalies intentionally.
* Document source schemas.

---

## Epic 4 — Data Ingestion

* Implement source readers.
* Implement raw loading.
* Implement ingestion metadata.
* Implement error handling.

---

## Epic 5 — Data Quality

* Implement validation rules.
* Implement quality metrics.
* Implement rejected-record handling.
* Generate quality reports.

---

## Epic 6 — Transformation

* Standardize data.
* Apply business rules.
* Prepare dimensions.
* Prepare facts.

---

## Epic 7 — Data Warehouse

* Create database schemas.
* Create dimensions.
* Create fact tables.
* Add indexes and constraints.
* Implement loading processes.

---

## Epic 8 — Analytics

* Define business KPIs.
* Implement analytical SQL.
* Create reusable analytical views.

---

## Epic 9 — Power BI

* Connect Power BI to curated data.
* Build semantic model.
* Build executive dashboard.
* Build operational dashboards.
* Validate KPI consistency.

---

## Epic 10 — Machine Learning

* Create ML dataset.
* Engineer features.
* Establish baseline.
* Train models.
* Evaluate models.
* Store predictions.
* Integrate predictions with BI/API.

---

## Epic 11 — API

* Implement FastAPI application.
* Implement health endpoint.
* Implement KPI endpoints.
* Implement analytical endpoints.
* Implement forecast endpoint.
* Add API tests.

---

## Epic 12 — Containerization

* Dockerize application services.
* Configure PostgreSQL.
* Configure API.
* Configure data services.
* Validate reproducibility.

---

## Epic 13 — Documentation

* Update README.
* Architecture diagrams.
* Data model diagrams.
* API documentation.
* Setup documentation.
* Architecture Decision Records.
* Project demonstration guide.

---

# 26. Eight-Week Development Plan

The project is designed around approximately 160 hours.

## Week 1 — Architecture and Data Modeling

Objectives:

* Finalize business requirements.
* Define business processes.
* Define entities.
* Define source schemas.
* Design Star Schema.
* Create architecture diagrams.
* Finalize repository structure.

Expected deliverables:

* SAD.
* Business requirements.
* Data model.
* Architecture diagrams.
* Initial data dictionary.

---

## Week 2 — Data Sources and Ingestion

Objectives:

* Generate realistic datasets.
* Implement ingestion pipelines.
* Implement raw storage.
* Implement ingestion metadata.

Expected deliverables:

* Source datasets.
* Ingestion module.
* Raw layer.

---

## Week 3 — Data Quality and Transformation

Objectives:

* Implement validation rules.
* Implement quality metrics.
* Build transformation pipelines.
* Prepare curated datasets.

Expected deliverables:

* Data quality framework.
* Transformation pipelines.
* Quality reports.

---

## Week 4 — Data Warehouse

Objectives:

* Implement PostgreSQL warehouse.
* Create dimensions.
* Create facts.
* Implement loading processes.
* Optimize analytical queries.

Expected deliverables:

* Operational schema.
* Star Schema.
* Warehouse loading pipeline.
* Data dictionary.

---

## Week 5 — BI and Analytics

Objectives:

* Define KPI catalog.
* Build analytical SQL.
* Build Power BI semantic model.
* Build dashboards.

Expected deliverables:

* KPI catalog.
* Power BI dashboards.
* Analytical views.

---

## Week 6 — Machine Learning

Objectives:

* Prepare ML dataset.
* Engineer features.
* Train baseline models.
* Evaluate models.
* Generate predictions.

Expected deliverables:

* ML pipeline.
* Model evaluation.
* Prediction dataset.

---

## Week 7 — API and Docker

Objectives:

* Build FastAPI service.
* Expose KPIs and predictions.
* Add API tests.
* Dockerize services.
* Validate end-to-end execution.

Expected deliverables:

* REST API.
* API documentation.
* Docker environment.

---

## Week 8 — Hardening and Presentation

Objectives:

* Testing.
* Bug fixing.
* Documentation.
* Architecture review.
* GitHub cleanup.
* Demo preparation.
* CV project description.
* Interview preparation.

Expected deliverables:

* Final GitHub repository.
* Complete documentation.
* Architecture diagrams.
* Demonstration.
* CV-ready project description.

---

# 27. Definition of Done

A feature is considered complete when:

* The implementation works.
* Relevant tests exist.
* Documentation is updated.
* Configuration is reproducible.
* Git history contains a meaningful commit.
* No unnecessary secrets or generated files are committed.

The complete project is considered finished when a new developer can clone the repository, follow the documentation, start the environment, execute the data pipeline, inspect the warehouse, access the API, and reproduce the main analytical outputs.

---

# 28. Architecture Decision Records

Important architectural decisions shall be documented using Architecture Decision Records (ADRs).

Initial decisions include:

### ADR-001 — PostgreSQL as Primary Data Platform

PostgreSQL is selected as the central relational platform because it provides mature SQL capabilities, strong data integrity, dimensional modeling support, and a realistic enterprise environment.

### ADR-002 — Python as Primary Data Engineering Language

Python is selected because of its ecosystem for data engineering, analytics, machine learning, and API development.

### ADR-003 — Star Schema for Analytical Modeling

Dimensional modeling is selected because it provides an intuitive structure for BI workloads and demonstrates fundamental data warehouse engineering skills.

### ADR-004 — Power BI for Business Intelligence

Power BI is selected to demonstrate enterprise BI and decision-support capabilities.

### ADR-005 — Docker for Reproducibility

Docker is selected to standardize the execution environment and demonstrate containerization skills.

### ADR-006 — Technology Expansion Only When Justified

Additional technologies such as PySpark, Airflow, Cloud, or GenAI shall only be introduced when they solve a clearly identified architectural problem or significantly improve the project's professional value.

---

# 29. Future Architecture Extensions

The platform is designed to support future evolution.

Potential future capabilities include:

* Distributed processing using PySpark.
* Workflow orchestration using Airflow.
* Cloud data warehouse deployment.
* Data lake architecture.
* Advanced ML pipelines.
* Model monitoring.
* MLOps capabilities.
* Streaming data ingestion.
* Natural-language analytical interfaces.

These capabilities are explicitly outside the minimum viable architecture and shall only be implemented when the core platform is stable.

---

# 30. Success Criteria

The project will be considered successful if it demonstrates the ability to:

1. Understand a realistic business process.
2. Design an appropriate data architecture.
3. Ingest heterogeneous operational data.
4. Implement measurable data quality controls.
5. Build reproducible ETL/ELT pipelines.
6. Design and populate a dimensional data warehouse.
7. Write advanced analytical SQL.
8. Build meaningful Power BI dashboards.
9. Develop and integrate a predictive model.
10. Expose analytical capabilities through an API.
11. Containerize the platform.
12. Test critical components.
13. Document architecture and technical decisions.
14. Explain every major technical choice during an interview.

---

# 31. Final Architecture Summary

The EODIP platform implements an end-to-end data value chain:

```text
                   BUSINESS OPERATIONS
                           |
                           v
                  DATA SOURCES
                           |
                           v
                  DATA INGESTION
                           |
                           v
                     RAW DATA
                           |
                           v
                   DATA QUALITY
                           |
                           v
                 TRANSFORMATION
                           |
                           v
                  DATA WAREHOUSE
                           |
             +-------------+-------------+
             |                           |
             v                           v
       BUSINESS INTELLIGENCE        MACHINE LEARNING
             |                           |
             v                           v
          POWER BI                  PREDICTIONS
             |                           |
             +-------------+-------------+
                           |
                           v
                        FASTAPI
                           |
                           v
                   DATA CONSUMERS
```

The architecture prioritizes:

* Data Engineering fundamentals.
* Business value.
* Data quality.
* Analytical modeling.
* Reproducibility.
* Maintainability.
* Professional software engineering practices.

The platform deliberately avoids unnecessary technological complexity and focuses on demonstrating the capabilities most relevant to a Data Engineering / Data / BI / AI PFE position.
