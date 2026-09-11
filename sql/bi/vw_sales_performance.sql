CREATE OR REPLACE VIEW dwh.vw_sales_performance AS

SELECT
    f.sales_key,
    f.sale_id,

    -- Date
    d.date_key,
    d.date,
    d.year,
    d.quarter,
    d.month,
    d.month_name,
    d.week,

    -- Product
    p.product_key,
    p.product_id,
    p.product_name,
    p.category,

    -- Customer
    c.customer_key,
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    c.country AS customer_country,
    c.city AS customer_city,

    -- Warehouse
    w.warehouse_key,
    w.warehouse_id,
    w.warehouse_name,
    w.country AS warehouse_country,
    w.city AS warehouse_city,

    -- Measures
    f.quantity,
    f.unit_price,
    f.discount,
    f.gross_amount,
    f.discount_amount,
    f.net_amount

FROM dwh.fact_sales f

INNER JOIN dwh.dim_date d
    ON f.date_key = d.date_key

INNER JOIN dwh.dim_product p
    ON f.product_key = p.product_key

INNER JOIN dwh.dim_customer c
    ON f.customer_key = c.customer_key

INNER JOIN dwh.dim_warehouse w
    ON f.warehouse_key = w.warehouse_key;