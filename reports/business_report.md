# Retail Sales Analytics — Business Report

## 1. Executive Summary

The cleaned Sample Superstore dataset contains **9,994 transaction lines**, **5,009 unique orders**, and **793 customers** after duplicate removal. Total revenue is **$2.30M**, total profit is **$286.4K**, and the weighted profit margin is **12.47%**.

The strongest commercial opportunities are in **Technology** and **Office Supplies**, while **Furniture** is a clear margin-management priority. Discounting is the largest profitability warning: transactions with discounts above 20% are loss-making in aggregate. The **Central** region also trails the other regions on weighted profit margin.

## 2. Key KPIs

| KPI | Result |
|---|---:|
| Transaction lines | 9,994 |
| Unique orders | 5,009 |
| Customers | 793 |
| Revenue | $2,297,200.86 |
| Profit | $286,397.02 |
| Weighted profit margin | 12.47% |
| Average discount | 15.62% |
| Units sold | 37,873 |
| Loss-making orders | 1,022 |

## 3. Key Findings

### 3.1 Category performance

- **Technology** is the largest category at **$836.2K revenue** and produces **$145.5K profit**, with a weighted margin of about **17.40%**.
- **Office Supplies** generates **$719.0K revenue** and **$122.5K profit**, with a margin of about **17.04%**.
- **Furniture** generates **$742.0K revenue** but only **$18.5K profit**, giving it a much weaker **2.49% margin**.

**Business implication:** Furniture requires SKU-level pricing, discount, and assortment review rather than simply pursuing more volume.

### 3.2 Discounting is strongly associated with margin erosion

| Discount band | Revenue | Profit | Margin |
|---|---:|---:|---:|
| No discount | $1,087.9K | $321.0K | 29.51% |
| 0–10% | $54.4K | $9.0K | 16.61% |
| 10–20% | $792.2K | $91.8K | 11.58% |
| 20–40% | $234.1K | **-$35.8K** | **-15.30%** |
| 40%+ | $128.6K | **-$99.6K** | **-77.40%** |

**Business implication:** High-discount transactions should be governed by category and product margin rules. Promotions above 20% should require a clear commercial justification.

### 3.3 Regional performance

- **West** leads revenue at **$725.5K** and has the strongest weighted margin at **14.94%**.
- **East** produces **$678.8K revenue** and a **13.48% margin**.
- **South** produces **$391.7K revenue** and an **11.93% margin**.
- **Central** produces **$501.2K revenue** but has the weakest margin at only **7.92%**.

**Business implication:** Central should be prioritized for a pricing, discount, product-mix, and operational review.

### 3.4 Customer profitability needs to be considered alongside sales

The highest-revenue customer is **Sean Miller**, with about **$25.0K sales**, but the account is loss-making at approximately **-$2.0K profit**.

This is an important management lesson: ranking customers only by revenue can hide unprofitable accounts. Customer dashboards should always show revenue, profit, margin, and order count together.

### 3.5 Seasonality

The strongest sales month in the dataset is **November 2018**, with approximately **$118.4K revenue**. The strongest profit month is **December 2017**, with approximately **$17.9K profit**.

This suggests that the business should plan inventory, staffing, and promotional activity around seasonal demand while protecting margin during high-volume periods.

## 4. Recommendations

1. **Introduce discount guardrails.** Flag transactions above 20% discount and require approval when expected margin falls below the target threshold.
2. **Fix Furniture profitability.** Review Tables and other low-margin Furniture sub-categories for excessive discounting, pricing gaps, and product costs.
3. **Protect high-value customers without rewarding unprofitable volume.** Use customer-level profit and margin, not sales alone, for account prioritization.
4. **Create a Central-region improvement plan.** Break the region down by state, category, customer segment, and discount band to isolate the margin problem.
5. **Scale high-margin categories.** Technology and Office Supplies combine meaningful revenue with approximately 17% weighted margins and should receive targeted growth investment.
6. **Use Power BI as the management layer.** Refresh the dashboard from the cleaned CSV or MySQL reporting view and monitor the KPIs above monthly.

## 5. Limitations

This is the public Sample Superstore dataset, so the analysis demonstrates analytical capability rather than representing a real company's confidential financial performance. Profit is the dataset's recorded profit field; actual management decisions would ideally incorporate returns, shipping cost, marketing cost, customer acquisition cost, and inventory data.
