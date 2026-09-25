# Data Model

Planned model tables:

- `fact_sales`
- `dim_customer`
- `dim_product`
- `dim_category`
- `dim_date`
- `exchange_rates`

Planned sales calculation:

```text
line_amount = UnitPrice * Quantity * (1 - Discount)
line_amount_sek = line_amount * exchange_rate_to_sek
```
