# Business Requirements Document

## Enterprise Operational Data Intelligence Platform (EODIP)

**Version:** 1.0
**Status:** Draft
**Author:** Data analytics team 
**Domain:** Supply Chain / Procurement / Inventory / Sales / Analytics

---

# 1. Document Purpose

This Business Requirements Document defines the business requirements, operational processes, actors, business events, information needs, and decision-support objectives of the Enterprise Operational Data Intelligence Platform (EODIP).

The document establishes the business foundation from which the platform's data model, data warehouse, analytical layer, machine learning capabilities, and APIs will be designed.

The objective is to ensure that every technical component of EODIP supports a clearly identified business requirement.

---

# 2. Business Vision

EODIP aims to provide an integrated view of operational performance across the supply chain.

The platform connects procurement, inbound logistics, warehousing, inventory, sales, and customer activity into a unified analytical environment.

The target business outcome is to enable decision-makers to answer questions such as:

* What are our current sales and revenue trends?
* Which products generate the most revenue and margin?
* Which suppliers perform best?
* How long do purchases take to arrive?
* Which products are at risk of stockout?
* Which products are slow-moving?
* Which warehouses hold the most inventory?
* How much inventory is currently available?
* What is expected demand in the coming periods?
* Which operational areas require attention?

---

# 3. Business Scope

## 3.1 In Scope

The initial platform covers the following business domains:

1. Supplier Management
2. Procurement
3. Import and Inbound Logistics
4. Warehouse Operations
5. Inventory Management
6. Customer Management
7. Sales
8. Business Performance
9. Demand Forecasting

---

## 3.2 Out of Scope

The following areas are outside the initial scope:

* Full accounting.
* Payroll.
* Human resources.
* Manufacturing.
* Real-time IoT monitoring.
* Customer-facing e-commerce.
* Full transportation management.
* Complex financial accounting.
* Production-grade cloud infrastructure.

These areas may be considered future extensions.

---

# 4. Business Actors

## 4.1 Management

Management requires high-level visibility into business performance.

Main information needs:

* Revenue.
* Margin.
* Sales growth.
* Inventory value.
* Procurement value.
* Supplier performance.
* Forecasted demand.

---

## 4.2 Procurement Manager

Responsible for purchasing products from suppliers.

Information needs:

* Supplier performance.
* Purchase history.
* Purchase prices.
* Lead times.
* Open purchase orders.
* Product demand.
* Supplier reliability.

---

## 4.3 Supply Chain / Logistics Manager

Responsible for inbound logistics and shipment monitoring.

Information needs:

* Shipment status.
* Expected arrival dates.
* Actual arrival dates.
* Supplier lead times.
* Delays.
* Transportation information.

---

## 4.4 Warehouse Manager

Responsible for warehouse operations and stock availability.

Information needs:

* Current stock.
* Stock movements.
* Stock value.
* Warehouse capacity indicators.
* Low-stock products.
* Slow-moving products.

---

## 4.5 Sales Manager

Responsible for sales performance.

Information needs:

* Revenue.
* Sales volume.
* Product performance.
* Customer performance.
* Sales trends.
* Margin.

---

## 4.6 Data / BI Analyst

Responsible for analytical exploration and reporting.

Information needs:

* Curated analytical datasets.
* Historical data.
* KPIs.
* Data quality information.
* Forecasts.

---

# 5. Core Business Process

The platform models the following end-to-end operational flow:

```text
Supplier
    ↓
Procurement
    ↓
Purchase Order
    ↓
Shipment / Import
    ↓
Warehouse Receipt
    ↓
Inventory
    ↓
Customer Order
    ↓
Sales
    ↓
Business Performance
    ↓
Forecasting
    ↓
Decision Support
```

This process represents the central business flow around which the data architecture will be designed.

---

# 6. Process 1 — Supplier Management

## 6.1 Objective

Maintain information about suppliers and evaluate supplier performance.

## 6.2 Main Activities

* Register suppliers.
* Maintain supplier information.
* Associate suppliers with products.
* Track purchase activity.
* Evaluate supplier reliability.

## 6.3 Business Data

Required information includes:

* Supplier identifier.
* Supplier name.
* Country.
* City.
* Contact information.
* Supplier category.
* Status.

## 6.4 Key Performance Indicators

Potential KPIs:

* Number of active suppliers.
* Purchase value by supplier.
* Average supplier lead time.
* On-time delivery rate.
* Number of delayed shipments.
* Supplier purchase volume.

---

# 7. Process 2 — Procurement

## 7.1 Objective

Manage purchasing activities required to replenish inventory.

## 7.2 Main Activities

```text
Demand / Stock Requirement
        ↓
Purchase Order
        ↓
Supplier Confirmation
        ↓
Shipment
        ↓
Receipt
```

## 7.3 Business Data

A purchase transaction may contain:

* Purchase order identifier.
* Supplier.
* Product.
* Order date.
* Expected delivery date.
* Quantity ordered.
* Unit purchase price.
* Total purchase value.
* Status.

## 7.4 Key Performance Indicators

* Total purchase value.
* Purchase volume.
* Average purchase price.
* Purchase orders by supplier.
* Average procurement lead time.
* Delayed purchase orders.

---

# 8. Process 3 — Import and Inbound Logistics

## 8.1 Objective

Track the movement of purchased goods from suppliers to warehouses.

## 8.2 Main Activities

```text
Purchase Order
      ↓
Shipment Creation
      ↓
Transportation
      ↓
Expected Arrival
      ↓
Actual Arrival
      ↓
Warehouse Receipt
```

## 8.3 Business Data

Potential information includes:

* Shipment identifier.
* Purchase order.
* Supplier.
* Origin.
* Destination.
* Shipment date.
* Expected arrival date.
* Actual arrival date.
* Transport mode.
* Shipment status.

## 8.4 Key Performance Indicators

* Average transit time.
* Average supplier lead time.
* On-time arrival rate.
* Delayed shipment count.
* Shipment volume.
* Shipment value.

---

# 9. Process 4 — Warehouse Operations

## 9.1 Objective

Track the reception and storage of products within warehouses.

## 9.2 Main Activities

* Receive goods.
* Register warehouse movements.
* Store products.
* Transfer products between warehouses where applicable.
* Dispatch products for sales.

## 9.3 Business Data

* Warehouse identifier.
* Product identifier.
* Receipt date.
* Quantity received.
* Movement type.
* Source/destination warehouse.
* Reference transaction.

---

# 10. Process 5 — Inventory Management

## 10.1 Objective

Maintain visibility over stock availability and inventory performance.

## 10.2 Main Activities

* Monitor stock levels.
* Track stock movements.
* Identify low-stock products.
* Identify excess inventory.
* Identify slow-moving products.
* Calculate inventory value.

## 10.3 Inventory Events

The platform will distinguish between inventory-affecting events such as:

```text
Purchase Receipt
       ↓
   Stock Increase

Sale
       ↓
   Stock Decrease

Warehouse Transfer
       ↓
Stock Movement

Adjustment
       ↓
Stock Correction
```

## 10.4 Key Performance Indicators

* Current stock quantity.
* Inventory value.
* Stock turnover.
* Days of inventory.
* Low-stock product count.
* Stockout count.
* Slow-moving inventory.
* Stock value by warehouse.

---

# 11. Process 6 — Customer Management

## 11.1 Objective

Maintain customer information and support customer-level sales analysis.

## 11.2 Business Data

* Customer identifier.
* Customer name.
* Customer category.
* City.
* Country.
* Customer status.

## 11.3 Analytical Requirements

The platform shall support analysis of:

* Revenue by customer.
* Sales volume by customer.
* Customer purchase frequency.
* Customer geographic distribution.
* Customer profitability where cost information is available.

---

# 12. Process 7 — Sales

## 12.1 Objective

Track customer sales and measure commercial performance.

## 12.2 Main Activities

```text
Customer
    ↓
Sales Order
    ↓
Order Lines
    ↓
Product Dispatch
    ↓
Sale
    ↓
Revenue
```

## 12.3 Business Data

A sales transaction may include:

* Sales order identifier.
* Customer.
* Product.
* Warehouse.
* Order date.
* Quantity sold.
* Unit selling price.
* Discount.
* Revenue.
* Cost.
* Margin.

## 12.4 Key Performance Indicators

* Revenue.
* Sales volume.
* Average selling price.
* Gross margin.
* Margin percentage.
* Sales growth.
* Revenue by product.
* Revenue by customer.
* Revenue by geography.

---

# 13. Process 8 — Business Performance

The platform will consolidate information from operational processes into a unified analytical layer.

## 13.1 Executive KPIs

The initial KPI catalog includes:

### Commercial

* Total Revenue.
* Sales Volume.
* Revenue Growth.
* Gross Margin.
* Margin Rate.

### Procurement

* Purchase Value.
* Purchase Volume.
* Average Purchase Price.
* Supplier Lead Time.

### Logistics

* Shipment Count.
* Average Transit Time.
* On-Time Delivery Rate.
* Delayed Shipment Count.

### Inventory

* Inventory Value.
* Current Stock.
* Inventory Turnover.
* Low-Stock Items.
* Slow-Moving Items.

### Customers

* Active Customers.
* Revenue per Customer.
* Top Customers.

### Suppliers

* Active Suppliers.
* Purchase Value per Supplier.
* Supplier Reliability.

---

# 14. Process 9 — Demand Forecasting

## 14.1 Objective

Use historical sales data to estimate future product demand.

The purpose is not to build a generic machine learning demonstration.

The purpose is to support inventory and procurement decisions.

---

## 14.2 Business Questions

The forecasting capability should help answer:

* What demand should we expect for a product?
* Which products may experience increased demand?
* Which products may require replenishment?
* How can expected demand support procurement planning?

---

## 14.3 Forecasting Flow

```text
Historical Sales
       ↓
Data Preparation
       ↓
Feature Engineering
       ↓
Forecast Model
       ↓
Future Demand
       ↓
Inventory / Procurement Decision Support
```

---

# 15. Business Events

The data model will be derived from measurable business events.

Important events include:

| Event                    | Description                               |
| ------------------------ | ----------------------------------------- |
| Supplier Registration    | A supplier becomes available              |
| Purchase Order Created   | A purchase request is issued              |
| Purchase Order Confirmed | Supplier confirms purchase                |
| Shipment Created         | Goods enter the inbound logistics process |
| Shipment Arrived         | Goods reach destination                   |
| Warehouse Receipt        | Goods are physically received             |
| Inventory Movement       | Stock changes                             |
| Sales Order Created      | Customer order is recorded                |
| Sale Completed           | Product is sold                           |
| Forecast Generated       | Future demand prediction is produced      |

These events form the basis of the analytical model.

---

# 16. Business Entities

The initial conceptual model includes:

```text
Supplier
Product
Category
Purchase Order
Purchase Order Line
Shipment
Warehouse
Inventory
Inventory Movement
Customer
Sales Order
Sales Order Line
Date
Location
Forecast
```

The final physical schema will be derived from these concepts after detailed modeling.

---

# 17. Business Relationships

The main conceptual relationships are:

```text
Supplier
   |
   | supplies
   v
Product

Supplier
   |
   | receives purchase orders
   v
Purchase Order
   |
   | contains
   v
Purchase Order Line
   |
   | references
   v
Product

Purchase Order
   |
   | generates
   v
Shipment
   |
   | received by
   v
Warehouse

Warehouse
   |
   | stores
   v
Inventory
   |
   | contains
   v
Product

Customer
   |
   | places
   v
Sales Order
   |
   | contains
   v
Sales Order Line
   |
   | references
   v
Product
```

---

# 18. Decision Support Requirements

The platform shall support operational and managerial decisions.

## 18.1 Procurement Decisions

Examples:

* Which products need replenishment?
* Which suppliers should receive more orders?
* Which suppliers experience frequent delays?
* How much should be purchased?

---

## 18.2 Inventory Decisions

Examples:

* Which products are approaching low-stock levels?
* Which products are slow-moving?
* Which warehouses contain excess inventory?
* Which products should be prioritized for replenishment?

---

## 18.3 Sales Decisions

Examples:

* Which products perform best?
* Which customers generate the most revenue?
* Which products have declining sales?
* Which geographic areas perform best?

---

## 18.4 Supply Chain Decisions

Examples:

* Which suppliers have the longest lead times?
* Which shipments are frequently delayed?
* Which routes or origins have higher transit times?

---

# 19. Business Rules

The initial business rules include:

## BR-01

A purchase order must reference a valid supplier.

## BR-02

A purchase order line must reference a valid product.

## BR-03

A sales order must reference a valid customer.

## BR-04

A sales order line must reference a valid product.

## BR-05

Quantities must be positive for normal purchase and sales transactions.

## BR-06

Product prices must not be negative.

## BR-07

Shipment arrival dates cannot precede shipment departure dates.

## BR-08

Inventory quantities must remain traceable through inventory movements.

## BR-09

Revenue must be derived consistently from quantity, price, and applicable discounts.

## BR-10

Forecasts must be associated with a defined product and forecast period.

---

# 20. Data Requirements

The platform requires data covering:

### Master Data

* Products.
* Product categories.
* Suppliers.
* Customers.
* Warehouses.
* Locations.

### Transactional Data

* Purchase orders.
* Purchase order lines.
* Shipments.
* Warehouse receipts.
* Inventory movements.
* Sales orders.
* Sales order lines.

### Analytical Data

* Daily sales aggregates.
* Inventory snapshots.
* Supplier performance metrics.
* Procurement metrics.
* Forecast results.

---

# 21. Data Quality Business Requirements

Data quality is considered part of the business process.

The platform must detect issues such as:

* Missing supplier identifiers.
* Missing product identifiers.
* Duplicate orders.
* Invalid quantities.
* Invalid prices.
* Invalid dates.
* Unknown product references.
* Unknown supplier references.
* Unknown customer references.
* Inconsistent inventory movements.

Rejected or suspicious records must be traceable.

---

# 22. Reporting Requirements

The BI platform shall provide at least four analytical perspectives.

## Executive Overview

Provides management with a high-level overview.

## Sales & Customers

Provides commercial analysis.

## Procurement & Suppliers

Provides purchasing and supplier analysis.

## Inventory & Supply Chain

Provides stock and operational analysis.

---

# 23. Analytical Grain Requirements

Every analytical fact must have a clearly defined grain.

Examples:

### Sales Fact

One row represents one product line within one sales transaction.

### Purchase Fact

One row represents one product line within one purchase order.

### Inventory Snapshot

One row represents the inventory position of one product at one warehouse for one date.

### Shipment Fact

One row represents one shipment transaction or shipment event according to the finalized logistics model.

The exact grain must be documented before physical implementation.

---

# 24. Forecasting Requirements

The forecasting dataset should contain sufficient historical information to support time-based prediction.

Minimum required information:

* Product.
* Date.
* Historical quantity sold.

Additional useful variables may include:

* Selling price.
* Promotions if available.
* Customer segment.
* Seasonality indicators.
* Product category.
* Warehouse.

The model shall be evaluated against a temporal validation strategy rather than a random split when appropriate.

---

# 25. Business Success Criteria

The platform will be considered successful from a business perspective if it enables a decision-maker to:

1. Obtain a consolidated view of operational performance.
2. Analyze historical sales.
3. Monitor inventory.
4. Evaluate suppliers.
5. Analyze procurement.
6. Identify operational anomalies.
7. Understand business trends.
8. Access demand forecasts.
9. Use consistent KPIs across reports.
10. Trace analytical information back to underlying data.

---

# 26. Traceability Matrix

The following mapping connects business needs to platform capabilities.

| Business Need                      | Platform Capability        |
| ---------------------------------- | -------------------------- |
| Centralized operational visibility | Data Warehouse             |
| Reliable data                      | Data Quality Layer         |
| Automated reporting                | BI Layer                   |
| Sales analysis                     | Sales Data Mart / Power BI |
| Inventory monitoring               | Inventory Analytics        |
| Supplier evaluation                | Procurement Analytics      |
| Logistics monitoring               | Shipment Analytics         |
| Demand planning                    | ML Forecasting             |
| Programmatic access                | FastAPI                    |
| Reproducible execution             | Docker                     |
| Technical traceability             | Git + Documentation        |

---

# 27. Requirements Prioritization

## Must Have

The following capabilities are mandatory:

* Data source generation.
* Data ingestion.
* Data quality.
* ETL/ELT.
* PostgreSQL data warehouse.
* Dimensional model.
* Analytical SQL.
* Power BI dashboards.
* One predictive ML use case.
* FastAPI.
* Docker.
* Automated tests.
* Documentation.

---

## Should Have

If sufficient development time remains:

* Incremental loading.
* Advanced data quality reporting.
* Pipeline execution metadata.
* PySpark implementation.
* Workflow orchestration.
* Cloud deployment.

---

## Could Have

Optional extensions:

* GenAI analytical assistant.
* Real-time ingestion.
* Advanced MLOps.
* Streaming architecture.

---

# 28. Business Requirements Baseline

The requirements defined in this document constitute the initial business baseline for EODIP.

Changes to the scope should be evaluated according to:

1. Business value.
2. Technical value.
3. Impact on development time.
4. Impact on architecture.
5. Relevance to the target Data Engineering / BI / AI roles.

Features that add complexity without meaningful business or technical value should not be implemented.

---

# 29. Next Design Phase

The next stage of the project is the conceptual data modeling phase.

The following artifacts will be produced:

1. Conceptual Data Model.
2. Entity definitions.
3. Relationship definitions.
4. Business event model.
5. Data dictionary.
6. Logical data model.
7. Star Schema.
8. Physical PostgreSQL schema.

No production data pipeline implementation should begin before the core data model has been reviewed and validated.
