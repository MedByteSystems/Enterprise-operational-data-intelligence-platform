CREATE OR REPLACE VIEW dwh.vw_purchase_performance AS

SELECT
    f.purchase_key,
    f.purchase_id,

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

    -- Supplier
    s.supplier_key,
    s.supplier_id,
    s.supplier_name,
    s.country AS supplier_country,
    s.city AS supplier_city,
    s.status AS supplier_status,

    -- Warehouse
    w.warehouse_key,
    w.warehouse_id,
    w.warehouse_name,
    w.country AS warehouse_country,
    w.city AS warehouse_city,

    -- Purchase measures
    f.quantity,
    f.unit_cost,
    f.purchase_amount,

    -- Delivery information
    f.order_date,
    f.expected_date,
    f.received_date,
    f.delivery_delay_days,
    f.delivery_status

FROM dwh.fact_purchases f

INNER JOIN dwh.dim_date d
    ON f.date_key = d.date_key

INNER JOIN dwh.dim_product p
    ON f.product_key = p.product_key

INNER JOIN dwh.dim_supplier s
    ON f.supplier_key = s.supplier_key

INNER JOIN dwh.dim_warehouse w
    ON f.warehouse_key = w.warehouse_key;