-- =============================================================
-- Retail Sales Analytics - MySQL Schema
-- Purpose: Create a normalized analytics-ready schema for retail
--          order, customer, product, and geography reporting.
-- MySQL Version: 8.0+ recommended for window functions and CTEs.
-- =============================================================

CREATE DATABASE IF NOT EXISTS retail_sales_analytics;
USE retail_sales_analytics;

-- Re-run safety for development environments.
DROP VIEW IF EXISTS vw_sales_enriched;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- Customer master data stores one row per customer.
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(150) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    country VARCHAR(100) DEFAULT 'United States',
    region VARCHAR(50) NOT NULL,
    state VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_customers_segment (segment),
    INDEX idx_customers_region_state (region, state)
);

-- Product master data stores product hierarchy and descriptive fields.
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    sub_category VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_products_category (category, sub_category)
);

-- Sales fact table stores one row per order line item.
CREATE TABLE sales (
    row_id INT PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE,
    ship_mode VARCHAR(100),
    customer_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    sales DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    quantity INT NOT NULL DEFAULT 0,
    discount DECIMAL(5,4) NOT NULL DEFAULT 0.0000,
    profit DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sales_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT fk_sales_product FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT chk_sales_non_negative CHECK (sales >= 0),
    CONSTRAINT chk_quantity_non_negative CHECK (quantity >= 0),
    CONSTRAINT chk_discount_range CHECK (discount >= 0 AND discount <= 1),
    INDEX idx_sales_order_date (order_date),
    INDEX idx_sales_order_id (order_id),
    INDEX idx_sales_customer (customer_id),
    INDEX idx_sales_product (product_id)
);

-- Enriched reporting view joins facts with customer and product dimensions.
CREATE OR REPLACE VIEW vw_sales_enriched AS
SELECT
    s.row_id,
    s.order_id,
    s.order_date,
    DATE_FORMAT(s.order_date, '%Y-%m') AS order_month,
    YEAR(s.order_date) AS order_year,
    MONTH(s.order_date) AS month_number,
    s.ship_date,
    s.ship_mode,
    c.customer_id,
    c.customer_name,
    c.segment,
    c.country,
    c.region,
    c.state,
    c.city,
    c.postal_code,
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,
    s.sales,
    s.quantity,
    s.discount,
    s.profit,
    CASE WHEN s.sales = 0 THEN 0 ELSE s.profit / s.sales END AS profit_margin
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
JOIN products p ON s.product_id = p.product_id;
