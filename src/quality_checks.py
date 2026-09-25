import pandas as pd


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def run_quality_checks(tables: dict[str, pd.DataFrame]) -> None:
    fact_sales = tables["fact_sales"]
    exchange_rates = tables["exchange_rates"]

    require(len(tables["dim_customer"]) > 0, "dim_customer is empty")
    require(len(tables["dim_product"]) > 0, "dim_product is empty")
    require(len(tables["dim_category"]) > 0, "dim_category is empty")
    require(len(fact_sales) > 0, "fact_sales is empty")
    require(fact_sales["order_id"].nunique() > 0, "fact_sales has no orders")
    require(not fact_sales["customer_id"].isna().any(), "fact_sales has missing customers")
    require(not fact_sales["category_id"].isna().any(), "fact_sales has missing categories")
    require(not fact_sales["exchange_rate_to_sek"].isna().any(), "fact_sales has missing exchange rates")
    require(not fact_sales["line_amount_sek"].isna().any(), "fact_sales has missing SEK amounts")
    require((fact_sales["line_amount_sek"] >= 0).all(), "fact_sales has negative SEK amounts")
    require(set(exchange_rates["order_year"]) == {1996, 1997, 1998}, "exchange rates do not cover 1996-1998")

    print(f"OK fact_sales rows: {len(fact_sales)}")
    print(f"OK distinct orders: {fact_sales['order_id'].nunique()}")
    print(f"OK total sales SEK: {fact_sales['line_amount_sek'].sum():,.2f}")
    print("OK exchange rates:")
    print(exchange_rates.to_string(index=False))