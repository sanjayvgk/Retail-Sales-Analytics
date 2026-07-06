-- =============================================================
-- Retail Sales Analytics - MySQL Query Library
-- Purpose: Portfolio-ready query examples and business analysis.
-- Assumption: Run schema.sql first and load data into customers,
--             products, and sales tables.
-- =============================================================

USE retail_sales_analytics;

-- =============================================================
-- BASIC QUERIES
-- =============================================================

-- SELECT: Preview the enriched sales view for data validation.
SELECT order_id, order_date, customer_name, product_name, sales, profit
FROM vw_sales_enriched;

-- WHERE: Find orders with negative profit that require margin review.
SELECT order_id, order_date, customer_name, product_name, sales, discount, profit
FROM vw_sales_enriched
WHERE profit < 0;

-- ORDER BY: Show the highest-value sales transactions first.
SELECT order_id, order_date, customer_name, product_name, sales
FROM vw_sales_enriched
ORDER BY sales DESC;

-- LIMIT: Return the 10 largest order lines by revenue for quick inspection.
SELECT order_id, product_name, category, sales, profit
FROM vw_sales_enriched
ORDER BY sales DESC
LIMIT 10;

-- =============================================================
-- INTERMEDIATE QUERIES
-- =============================================================

-- GROUP BY with aggregates: Summarize revenue, profit, and order count by category.
SELECT
    category,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders
FROM vw_sales_enriched
GROUP BY category
ORDER BY total_revenue DESC;

-- HAVING: Identify product sub-categories generating meaningful revenue but weak profit.
SELECT
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0), 4) AS profit_margin
FROM vw_sales_enriched
GROUP BY category, sub_category
HAVING SUM(sales) >= 10000 AND SUM(profit) < 0
ORDER BY total_profit ASC;

-- Aggregate Functions: Calculate overall KPIs for executive reporting.
SELECT
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(AVG(discount), 4) AS average_discount,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0), 4) AS profit_margin
FROM vw_sales_enriched;

-- =============================================================
-- ADVANCED SQL QUERIES
-- =============================================================

-- CTE: Build monthly KPIs once, then calculate profit margin from the result.
WITH monthly_kpis AS (
    SELECT
        order_month,
        SUM(sales) AS monthly_revenue,
        SUM(profit) AS monthly_profit,
        COUNT(DISTINCT order_id) AS monthly_orders
    FROM vw_sales_enriched
    GROUP BY order_month
)
SELECT
    order_month,
    ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(monthly_profit, 2) AS monthly_profit,
    monthly_orders,
    ROUND(monthly_profit / NULLIF(monthly_revenue, 0), 4) AS monthly_profit_margin
FROM monthly_kpis
ORDER BY order_month;

-- Window Function - Running Totals: Track cumulative revenue over time.
WITH monthly_sales AS (
    SELECT order_month, SUM(sales) AS monthly_revenue
    FROM vw_sales_enriched
    GROUP BY order_month
)
SELECT
    order_month,
    ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(SUM(monthly_revenue) OVER (ORDER BY order_month), 2) AS running_revenue
FROM monthly_sales
ORDER BY order_month;

-- Ranking: Rank products within each category by revenue.
SELECT
    category,
    product_name,
    ROUND(SUM(sales), 2) AS total_revenue,
    RANK() OVER (PARTITION BY category ORDER BY SUM(sales) DESC) AS category_revenue_rank
FROM vw_sales_enriched
GROUP BY category, product_name
ORDER BY category, category_revenue_rank;

-- View usage: Query the enriched reporting view for a reusable BI-ready dataset.
SELECT order_month, region, category, SUM(sales) AS revenue, SUM(profit) AS profit
FROM vw_sales_enriched
GROUP BY order_month, region, category
ORDER BY order_month, region, category;

-- =============================================================
-- BUSINESS QUERIES
-- =============================================================

-- Total Revenue: Calculate total company revenue across all transactions.
SELECT ROUND(SUM(sales), 2) AS total_revenue
FROM vw_sales_enriched;

-- Monthly Revenue: Show sales trend by month.
SELECT order_month, ROUND(SUM(sales), 2) AS monthly_revenue
FROM vw_sales_enriched
GROUP BY order_month
ORDER BY order_month;

-- Monthly Profit: Show profitability trend by month.
SELECT order_month, ROUND(SUM(profit), 2) AS monthly_profit
FROM vw_sales_enriched
GROUP BY order_month
ORDER BY order_month;

-- Top Customers: Identify customers contributing the most revenue and profit.
SELECT
    customer_id,
    customer_name,
    segment,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS order_count
FROM vw_sales_enriched
GROUP BY customer_id, customer_name, segment
ORDER BY total_revenue DESC
LIMIT 20;

-- Top Products: Identify the highest-revenue products.
SELECT
    product_id,
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity) AS units_sold
FROM vw_sales_enriched
GROUP BY product_id, product_name, category, sub_category
ORDER BY total_revenue DESC
LIMIT 20;

-- Category Analysis: Compare revenue, profit, units, and margin by category.
SELECT
    category,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity) AS units_sold,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0), 4) AS profit_margin
FROM vw_sales_enriched
GROUP BY category
ORDER BY total_revenue DESC;

-- Region Analysis: Evaluate performance across major sales regions.
SELECT
    region,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(discount), 4) AS average_discount
FROM vw_sales_enriched
GROUP BY region
ORDER BY total_revenue DESC;

-- State Analysis: Find top and bottom state-level markets by profit.
SELECT
    state,
    region,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0), 4) AS profit_margin
FROM vw_sales_enriched
GROUP BY state, region
ORDER BY total_profit DESC;

-- Discount Analysis: Quantify how discount bands affect profitability.
SELECT
    CASE
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount <= 0.10 THEN 'Low Discount (1%-10%)'
        WHEN discount <= 0.20 THEN 'Moderate Discount (11%-20%)'
        WHEN discount <= 0.40 THEN 'High Discount (21%-40%)'
        ELSE 'Very High Discount (>40%)'
    END AS discount_band,
    ROUND(AVG(discount), 4) AS average_discount,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0), 4) AS profit_margin
FROM vw_sales_enriched
GROUP BY discount_band
ORDER BY average_discount;

-- Profit Margin: Calculate margin by category and region to identify strong combinations.
SELECT
    category,
    region,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0), 4) AS profit_margin
FROM vw_sales_enriched
GROUP BY category, region
ORDER BY profit_margin DESC;

-- Customer Segmentation: Segment customers by lifetime revenue for targeting.
WITH customer_value AS (
    SELECT
        customer_id,
        customer_name,
        segment,
        SUM(sales) AS lifetime_revenue,
        SUM(profit) AS lifetime_profit,
        COUNT(DISTINCT order_id) AS lifetime_orders
    FROM vw_sales_enriched
    GROUP BY customer_id, customer_name, segment
)
SELECT
    customer_id,
    customer_name,
    segment,
    ROUND(lifetime_revenue, 2) AS lifetime_revenue,
    ROUND(lifetime_profit, 2) AS lifetime_profit,
    lifetime_orders,
    CASE
        WHEN lifetime_revenue >= 10000 THEN 'VIP'
        WHEN lifetime_revenue >= 5000 THEN 'High Value'
        WHEN lifetime_revenue >= 1000 THEN 'Growth'
        ELSE 'Low Value'
    END AS customer_value_segment
FROM customer_value
ORDER BY lifetime_revenue DESC;
