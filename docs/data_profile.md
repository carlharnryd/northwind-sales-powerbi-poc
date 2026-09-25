# Data Profile

Snapshot from local validation on 2026-09-25.

## Source Counts

Northwind raw extraction follows OData pagination through `@odata.nextLink`.

| Source entity | Rows |
| --- | ---: |
| Customers | 91 |
| Orders | 830 |
| Order_Details | 2,155 |
| Products | 77 |
| Categories | 8 |

Riksbank raw extraction:

| Year | Observations | Series | USD/SEK selected date | USD/SEK rate |
| ---: | ---: | ---: | --- | ---: |
| 1996 | 64 | 32 | 1996-12-30 | 6.870 |
| 1997 | 64 | 32 | 1997-12-30 | 7.870 |
| 1998 | 135 | 45 | 1998-12-30 | 8.065 |

## Model Counts

| Table | Rows |
| --- | ---: |
| fact_sales | 2,155 |
| dim_customer | 91 |
| dim_product | 77 |
| dim_category | 8 |
| dim_date | 672 |
| exchange_rates | 3 |

## Sales Summary

- Order date range: 1996-07-04 to 1998-05-06.
- Distinct orders: 830.
- Customers with sales: 89 of 91.
- Products sold: 77 of 77.
- Categories sold: 8 of 8.
- Original total sales amount: 1,265,793.04.
- Total sales in SEK: 9,839,628.90.
- Average order value in SEK: 11,854.97.

## Sales by Year

| Year | Orders | Order lines | Sales SEK |
| ---: | ---: | ---: | ---: |
| 1996 | 152 | 405 | 1,429,536.87 |
| 1997 | 408 | 1,059 | 4,856,460.55 |
| 1998 | 270 | 691 | 3,553,631.48 |

Note: 1998 only includes orders through 1998-05-06, so it is not a full calendar year.

## Top Categories

| Category | Sales SEK |
| --- | ---: |
| Beverages | 2,082,828.43 |
| Dairy Products | 1,819,829.03 |
| Confections | 1,298,143.53 |
| Meat/Poultry | 1,264,552.86 |
| Seafood | 1,022,396.35 |

## Top Customers

| Customer | Country | Sales SEK |
| --- | --- | ---: |
| QUICK-Stop | Germany | 863,189.69 |
| Save-a-lot Markets | USA | 818,070.75 |
| Ernst Handel | Austria | 817,834.09 |
| Rattlesnake Canyon Grocery | USA | 395,805.37 |
| Hungry Owl All-Night Grocers | Ireland | 388,196.89 |

## Top Countries

| Country | Orders | Customers | Sales SEK |
| --- | ---: | ---: | ---: |
| USA | 122 | 13 | 1,912,708.78 |
| Germany | 122 | 11 | 1,792,056.60 |
| Austria | 40 | 2 | 990,563.99 |
| Brazil | 83 | 9 | 830,100.02 |
| France | 77 | 10 | 626,568.06 |

## Quality Checks

- Missing customer keys in fact table: 0.
- Missing product keys in fact table: 0.
- Missing category keys in fact table: 0.
- Missing exchange rates: 0.
- Missing SEK amounts: 0.
- Negative SEK amounts: 0.
- Orphan customer/product/category/date relationships: 0.

Customers without sales:

- `FISSA` - FISSA Fabrica Inter. Salchichas S.A., Spain.
- `PARIS` - Paris specialites, France.

## Report Implications

- Page 1 should highlight Beverages and Dairy Products as the two strongest categories.
- Page 1 should include a sales-over-time chart, but the report should avoid comparing 1998 as a complete year because the data stops in May.
- Page 2 should call out that USA and Germany are the largest markets by SEK sales.
- Top customer rankings are concentrated: the top three customers are close to each other and clearly above the rest.
