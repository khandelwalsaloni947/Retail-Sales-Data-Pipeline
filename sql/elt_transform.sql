-- Reset tables
DELETE FROM sales_report_elt;
INSERT INTO sales_report_elt (
    order_id,
    order_date,
    customer_id,
    customer_name,
    city,
    product_id,
    product_name,
    category,
    quantity,
    price,
    total_amount
)
SELECT
    CAST(ro.order_id AS INTEGER) AS order_id,
    CAST(ro.order_date AS DATE) AS order_date,
    CAST(ro.customer_id AS INTEGER) AS customer_id,
    INITCAP(TRIM(rc.customer_name)) AS customer_name,
    INITCAP(TRIM(rc.city)) AS city,
    CAST(ro.product_id AS INTEGER) AS product_id,
    INITCAP(TRIM(rp.product_name)) AS product_name,
    INITCAP(TRIM(rp.category)) AS category,
    CAST(ro.quantity AS INTEGER) AS quantity,
    CAST(rp.price AS NUMERIC(10,2)) AS price,
    CAST(ro.quantity AS INTEGER) * CAST(rp.price AS NUMERIC(10,2)) AS total_amount
FROM raw_orders ro
JOIN raw_customers rc
    ON ro.customer_id = rc.customer_id
JOIN raw_products rp
    ON ro.product_id = rp.product_id
WHERE ro.order_id ~ '^[0-9]+$'
  AND ro.customer_id ~ '^[0-9]+$'
  AND ro.product_id ~ '^[0-9]+$'
  AND ro.quantity ~ '^[0-9]+$'
  AND rp.price ~ '^[0-9]+(\.[0-9]+)?$';


DELETE FROM category_summary_elt;

INSERT INTO category_summary_elt (category, total_revenue)
SELECT category, SUM(total_amount)
FROM sales_report_elt
GROUP BY category;