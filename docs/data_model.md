# Data Model

Planned model tables:

- `fact_sales`
- `dim_customer`
- `dim_product`
- `dim_category`
- `dim_date`
- `exchange_rates`

The report should use the first five tables. `exchange_rates` is kept as a
supporting audit table in the local warehouse.

Main relationships for Power BI:

- `fact_sales[customer_id]` -> `dim_customer[customer_id]`
- `fact_sales[product_id]` -> `dim_product[product_id]`
- `fact_sales[category_id]` -> `dim_category[category_id]`
- `fact_sales[order_date]` -> `dim_date[date]`

Planned sales calculation:

```text
line_amount = UnitPrice * Quantity * (1 - Discount)
line_amount_sek = line_amount * exchange_rate_to_sek
```

Suggested Power BI measures:

```DAX
Total Sales SEK = SUM(fact_sales[line_amount_sek])

Order Count = DISTINCTCOUNT(fact_sales[order_id])

Average Order Value SEK = DIVIDE([Total Sales SEK], [Order Count])
```
