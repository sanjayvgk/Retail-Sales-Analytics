-- Load the generated CSV exports into MySQL 8.0+.
-- Run this file from the repository root after executing schema.sql.
-- If LOCAL INFILE is disabled, enable it in the MySQL client/server settings.

USE retail_sales_analytics;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE sales;
TRUNCATE TABLE products;
TRUNCATE TABLE customers;
SET FOREIGN_KEY_CHECKS = 1;

LOAD DATA LOCAL INFILE 'data/processed/mysql/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(customer_id, customer_name, segment, country, region, state, city, postal_code);

LOAD DATA LOCAL INFILE 'data/processed/mysql/products.csv'
INTO TABLE products
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(product_id, product_name, category, sub_category);

LOAD DATA LOCAL INFILE 'data/processed/mysql/sales.csv'
INTO TABLE sales
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(row_id, order_id, order_date, ship_date, ship_mode, customer_id, product_id, sales, quantity, discount, profit);

SELECT COUNT(*) AS customer_rows FROM customers;
SELECT COUNT(*) AS product_rows FROM products;
SELECT COUNT(*) AS sales_rows FROM sales;
SELECT ROUND(SUM(sales), 2) AS total_sales, ROUND(SUM(profit), 2) AS total_profit FROM sales;
