# Power BI Dashboard Build Guide

This guide explains how to build a professional retail analytics report in Power BI using the cleaned Python output or the SQL reporting view `vw_sales_enriched`.

## 1. Data Connection and Model Setup

1. Open Power BI Desktop.
2. Select **Get Data** and connect to either:
   - CSV/Excel output from the Python analytics pipeline, or
   - MySQL database table/view `vw_sales_enriched`.
3. Confirm the following data types:
   - `order_date`: Date
   - `order_month`: Text or Date month key
   - `sales`, `profit`, `discount`: Decimal number
   - `quantity`: Whole number
4. Create DAX measures:

```DAX
Total Revenue = SUM(vw_sales_enriched[sales])
Total Profit = SUM(vw_sales_enriched[profit])
Total Orders = DISTINCTCOUNT(vw_sales_enriched[order_id])
Average Discount = AVERAGE(vw_sales_enriched[discount])
Profit Margin = DIVIDE([Total Profit], [Total Revenue])
Total Quantity = SUM(vw_sales_enriched[quantity])
Customers = DISTINCTCOUNT(vw_sales_enriched[customer_id])
```

## 2. Global Report Design Standards

- Use a consistent 16:9 canvas.
- Add a top title bar with the dashboard name and last refresh date.
- Use a clean white or light gray background.
- Use 2-3 brand colors consistently, for example navy, teal, and gray.
- Keep slicers aligned on the left side or across the top.
- Apply currency formatting to revenue and profit measures.
- Apply percentage formatting to discount and profit margin measures.
- Use tooltips to show `Total Revenue`, `Total Profit`, `Profit Margin`, and `Total Orders` where relevant.

## Dashboard 1: Executive Summary

### Purpose
Provide leadership with a high-level view of revenue, profit, order volume, discounting, and trend performance.

### Slicers
Add slicers across the top row:
- `order_year`
- `region`
- `category`
- `segment`

### Cards
Use **Card** visuals in the first row:
1. **Total Revenue**
   - Field: `Total Revenue`
2. **Total Profit**
   - Field: `Total Profit`
3. **Total Orders**
   - Field: `Total Orders`
4. **Average Discount**
   - Field: `Average Discount`

### Charts
1. **Monthly Sales Trend**
   - Visual: Line chart
   - X-axis: `order_month`
   - Y-axis: `Total Revenue`
   - Filter: optional `order_year`

2. **Monthly Profit Trend**
   - Visual: Line chart
   - X-axis: `order_month`
   - Y-axis: `Total Profit`
   - Conditional formatting: use red for negative profit if available

3. **Category Sales**
   - Visual: Clustered bar chart
   - Y-axis: `category`
   - X-axis: `Total Revenue`
   - Tooltip: `Total Profit`, `Profit Margin`

4. **Region Sales**
   - Visual: Filled map or clustered column chart
   - Location/Axis: `region`
   - Values: `Total Revenue`
   - Tooltip: `Total Profit`, `Total Orders`

### Professional Layout
- Row 1: Four KPI cards.
- Row 2: Monthly Sales Trend and Monthly Profit Trend side by side.
- Row 3: Category Sales and Region Sales side by side.

## Dashboard 2: Customer Insights

### Purpose
Identify high-value customers, customer segments, and buying behavior.

### Slicers
- `segment`
- `region`
- `state`
- `order_year`

### Visuals
1. **Top Customers by Revenue**
   - Visual: Bar chart
   - Y-axis: `customer_name`
   - X-axis: `Total Revenue`
   - Visual-level filter: Top N = 10 by `Total Revenue`

2. **Customer Segment Revenue**
   - Visual: Donut chart or stacked column chart
   - Legend/Axis: `segment`
   - Values: `Total Revenue`

3. **Customer Profitability Table**
   - Visual: Table or matrix
   - Columns: `customer_name`, `segment`, `Total Revenue`, `Total Profit`, `Profit Margin`, `Total Orders`
   - Conditional formatting: highlight negative profit in red

4. **Orders by Customer Segment Over Time**
   - Visual: Line and clustered column chart
   - X-axis: `order_month`
   - Column values: `Total Orders`
   - Line values: `Total Revenue`
   - Legend: `segment`

### Professional Layout
- Place customer slicers on the left panel.
- Put segment summary visuals on top.
- Use the customer profitability table across the bottom for drill-down analysis.

## Dashboard 3: Product Performance

### Purpose
Evaluate product, category, and sub-category contribution to revenue and profit.

### Slicers
- `category`
- `sub_category`
- `region`
- `order_year`

### Visuals
1. **Top Products by Revenue**
   - Visual: Bar chart
   - Y-axis: `product_name`
   - X-axis: `Total Revenue`
   - Visual-level filter: Top N = 15 by `Total Revenue`

2. **Category and Sub-Category Matrix**
   - Visual: Matrix
   - Rows: `category`, `sub_category`
   - Values: `Total Revenue`, `Total Profit`, `Profit Margin`, `Total Quantity`

3. **Product Profitability Scatter Plot**
   - Visual: Scatter chart
   - X-axis: `Total Revenue`
   - Y-axis: `Total Profit`
   - Size: `Total Quantity`
   - Legend: `category`
   - Details: `product_name`

4. **Discount vs Profit Margin**
   - Visual: Scatter chart
   - X-axis: `Average Discount`
   - Y-axis: `Profit Margin`
   - Legend: `category`
   - Details: `sub_category`

### Professional Layout
- Use the scatter plot as the central analytical visual.
- Place top product chart on the left and category matrix on the right.
- Put discount analysis at the bottom to support pricing decisions.

## Dashboard 4: Regional Analysis

### Purpose
Compare market performance by region, state, and city to guide regional growth plans.

### Slicers
- `region`
- `state`
- `category`
- `segment`
- `order_year`

### Visuals
1. **Revenue by Region**
   - Visual: Clustered column chart
   - X-axis: `region`
   - Y-axis: `Total Revenue`
   - Tooltip: `Total Profit`, `Profit Margin`

2. **State Performance Map**
   - Visual: Filled map
   - Location: `state`
   - Values: `Total Revenue`
   - Tooltip: `Total Profit`, `Total Orders`, `Average Discount`

3. **State Profitability Ranking**
   - Visual: Bar chart
   - Y-axis: `state`
   - X-axis: `Total Profit`
   - Visual-level filter: Top N = 15 by `Total Profit`

4. **Region and Category Matrix**
   - Visual: Matrix
   - Rows: `region`
   - Columns: `category`
   - Values: `Total Revenue`, `Total Profit`

### Professional Layout
- Put the map at the center for geographic storytelling.
- Put KPI cards for selected region above the map.
- Place the ranking chart and matrix below for detailed comparison.
