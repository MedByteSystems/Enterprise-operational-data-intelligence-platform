CREATE OR REPLACE VIEW dwh.vw_supply_chain_performance AS

WITH sales_agg AS (

    SELECT
        date_key,
        product_key,
        warehouse_key,

        SUM(quantity) AS sold_quantity,
        SUM(net_amount) AS sales_amount,
        COUNT(*) AS sales_count

    FROM dwh.fact_sales

    GROUP BY
        date_key,
        product_key,
        warehouse_key
),

purchase_agg AS (

    SELECT
        date_key,
        product_key,
        warehouse_key,

        SUM(quantity) AS purchased_quantity,
        SUM(purchase_amount) AS purchase_amount,
        COUNT(*) AS purchase_count,

        AVG(delivery_delay_days)
            AS avg_delivery_delay_days,

        COUNT(*) FILTER (
            WHERE delivery_status = 'LATE'
        ) AS late_purchase_count,

        COUNT(*) FILTER (
            WHERE delivery_status = 'ON_TIME'
        ) AS on_time_purchase_count

    FROM dwh.fact_purchases

    GROUP BY
        date_key,
        product_key,
        warehouse_key
)

SELECT

    d.date_key,
    d.date,
    d.year,
    d.quarter,
    d.month,
    d.month_name,
    d.week,

    p.product_key,
    p.product_id,
    p.product_name,
    p.category,

    w.warehouse_key,
    w.warehouse_id,
    w.warehouse_name,
    w.country AS warehouse_country,
    w.city AS warehouse_city,

    -- Sales
    COALESCE(sa.sold_quantity, 0)
        AS sold_quantity,

    COALESCE(sa.sales_amount, 0)
        AS sales_amount,

    COALESCE(sa.sales_count, 0)
        AS sales_count,

    -- Purchases
    COALESCE(pa.purchased_quantity, 0)
        AS purchased_quantity,

    COALESCE(pa.purchase_amount, 0)
        AS purchase_amount,

    COALESCE(pa.purchase_count, 0)
        AS purchase_count,

    -- Delivery performance
    COALESCE(
        pa.avg_delivery_delay_days,
        0
    ) AS avg_delivery_delay_days,

    COALESCE(
        pa.late_purchase_count,
        0
    ) AS late_purchase_count,

    COALESCE(
        pa.on_time_purchase_count,
        0
    ) AS on_time_purchase_count,

    -- Derived KPI
    CASE
        WHEN COALESCE(pa.purchase_count, 0) > 0
        THEN
            pa.late_purchase_count::DECIMAL
            / pa.purchase_count
        ELSE 0
    END AS late_purchase_rate

FROM dwh.dim_date d

CROSS JOIN dwh.dim_product p

CROSS JOIN dwh.dim_warehouse w

LEFT JOIN sales_agg sa
    ON sa.date_key = d.date_key
    AND sa.product_key = p.product_key
    AND sa.warehouse_key = w.warehouse_key

LEFT JOIN purchase_agg pa
    ON pa.date_key = d.date_key
    AND pa.product_key = p.product_key
    AND pa.warehouse_key = w.warehouse_key

WHERE
    sa.date_key IS NOT NULL
    OR pa.date_key IS NOT NULL;