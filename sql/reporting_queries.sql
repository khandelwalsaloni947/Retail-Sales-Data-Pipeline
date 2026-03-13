-- reporting_queries.sql

-- 1️ Total number of rows in the final sales report
SELECT COUNT(*) AS total_orders
FROM sales_report_elt;

-- 2️ Sample data from the final sales report
SELECT *
FROM sales_report_elt
LIMIT 10;

-- 3️ Total revenue by product category
SELECT category, SUM(total_amount) AS total_revenue
FROM sales_report_elt
GROUP BY category
ORDER BY total_revenue DESC;

-- 4️ Total number of orders by city
SELECT city, COUNT(*) AS total_orders
FROM sales_report_elt
GROUP BY city
ORDER BY total_orders DESC;