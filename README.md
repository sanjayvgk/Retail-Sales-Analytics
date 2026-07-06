# Retail Sales Analytics

A professional retail sales analytics and business intelligence portfolio project using **Python**, **MySQL**, and **Power BI**. The project is designed for Data Analyst and Business Intelligence roles and demonstrates end-to-end analytical thinking: data preparation, SQL analysis, dashboard design, and business recommendations.

## Project Overview

Retail organizations need reliable insight into revenue, profitability, customers, products, discounts, and regional performance. This project provides a complete analytics framework for answering key business questions and communicating findings to stakeholders.

The Python analytics pipeline has been completed separately. This repository now includes the remaining production-quality deliverables: a complete MySQL solution, Power BI dashboard build guide, business report, and professional documentation.

## Objectives

- Analyze retail revenue and profit performance.
- Identify top customers, products, categories, and regions.
- Evaluate discount impact on profitability.
- Segment customers by lifetime value.
- Provide SQL queries for repeatable business analysis.
- Document Power BI dashboards that executives and analysts can build.
- Summarize insights and recommendations in a business report.

## Folder Structure

```text
Retail-Sales-Analytics/
├── README.md
├── data/                         # Raw or processed datasets, if included
├── notebooks/                    # Python notebooks, if included
├── powerbi/
│   └── dashboard_guide.md        # Step-by-step Power BI dashboard guide
├── reports/
│   └── business_report.md        # Senior business analyst report
├── sql/
│   ├── schema.sql                # MySQL database schema and reporting view
│   └── queries.sql               # SQL query library for analysis
├── src/                          # Python source code, if included
└── visuals/                      # Dashboard screenshots or exported visuals
```

## Technology Stack

- **Python**: Data cleaning, exploratory data analysis, and analytics pipeline.
- **MySQL 8.0+**: Relational schema, reporting view, CTEs, window functions, aggregations, and business queries.
- **Power BI**: Executive dashboards and self-service reporting.
- **Markdown**: Professional documentation and business reporting.
- **Git/GitHub**: Version control and portfolio presentation.

## Project Workflow

1. **Data Collection**
   - Obtain retail transaction data with order, customer, product, geography, sales, discount, and profit fields.

2. **Python Analysis**
   - Clean and transform raw data.
   - Validate data types and missing values.
   - Create derived fields for analysis.
   - Export analysis-ready data for SQL and BI tools.

3. **SQL Modeling and Analysis**
   - Build a MySQL schema with customer, product, and sales tables.
   - Create an enriched reporting view.
   - Run reusable queries for revenue, profit, rankings, trends, segmentation, and discount analysis.

4. **Power BI Dashboarding**
   - Connect Power BI to the analysis-ready dataset or MySQL view.
   - Build dashboards for executives, customers, products, and regional leaders.
   - Add slicers, filters, KPI cards, charts, maps, and tables.

5. **Business Reporting**
   - Convert technical analysis into business insights.
   - Recommend practical actions for revenue growth and margin improvement.

## Python Analysis

The Python analytics pipeline supports data preparation and exploratory analysis. Typical outputs include cleaned retail datasets, KPI summaries, and validation checks that can be loaded into MySQL or Power BI.

Recommended Python tasks include:

- Standardizing column names.
- Converting order and ship dates to date types.
- Handling missing postal codes or geography values.
- Creating monthly fields.
- Validating sales, profit, quantity, and discount ranges.
- Exporting clean data for SQL ingestion.

## SQL Analysis

The SQL deliverables are located in the `sql/` folder:

- `sql/schema.sql`: Creates the MySQL database, customer table, product table, sales fact table, indexes, constraints, and enriched reporting view.
- `sql/queries.sql`: Provides commented queries covering basic SQL, intermediate aggregation, advanced analytics, and business use cases.

SQL topics covered:

- `SELECT`, `WHERE`, `ORDER BY`, and `LIMIT`
- `GROUP BY`, `HAVING`, and aggregate functions
- CTEs and window functions
- Ranking and running totals
- Views
- Revenue, profit, customer, product, category, region, state, discount, margin, and segmentation analysis

## Power BI Dashboard

The Power BI guide is located at `powerbi/dashboard_guide.md`. It explains how to build four dashboards without generating a `.pbix` file:

1. **Executive Summary**
   - KPI cards for revenue, profit, orders, and discount.
   - Monthly sales and profit trends.
   - Category and region sales visuals.

2. **Customer Insights**
   - Top customers.
   - Customer segment revenue.
   - Customer profitability table.
   - Segment order trends.

3. **Product Performance**
   - Top products.
   - Category and sub-category matrix.
   - Product profitability scatter plot.
   - Discount vs profit margin analysis.

4. **Regional Analysis**
   - Region revenue.
   - State performance map.
   - State profitability ranking.
   - Region/category matrix.

## Business Insights

The business report is located at `reports/business_report.md`. It includes:

- Executive summary
- Business problems
- Key insights
- Recommendations
- Future improvements

Core business themes include margin management, customer prioritization, product portfolio optimization, regional performance monitoring, and discount governance.

## How to Run

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Retail-Sales-Analytics
```

### 2. Run the MySQL Schema

```bash
mysql -u <username> -p < sql/schema.sql
```

### 3. Load Data

Load cleaned customer, product, and sales data into the corresponding MySQL tables. The schema expects:

- `customers`: customer and geography fields
- `products`: product hierarchy fields
- `sales`: transaction-level order line fields

### 4. Run SQL Analysis

```bash
mysql -u <username> -p retail_sales_analytics < sql/queries.sql
```

### 5. Build Power BI Dashboards

Open Power BI Desktop, connect to the cleaned dataset or MySQL `vw_sales_enriched` view, and follow `powerbi/dashboard_guide.md`.

## Screenshots Section

Add dashboard screenshots to the `visuals/` folder when the Power BI report is built.

Suggested screenshots:

- `visuals/executive_summary.png`
- `visuals/customer_insights.png`
- `visuals/product_performance.png`
- `visuals/regional_analysis.png`

## Future Enhancements

- Add automated data ingestion into MySQL.
- Add Python unit tests for data quality checks.
- Add sales forecasting and seasonal decomposition.
- Add customer retention and cohort analysis.
- Add Power BI row-level security by region.
- Add dashboard screenshots and a published Power BI link.
- Add CI checks for SQL formatting and documentation validation.
