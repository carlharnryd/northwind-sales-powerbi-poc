import json
from pathlib import Path

import pandas as pd

from src.config import RAW_NORTHWIND_DIR, RAW_RIKSBANK_DIR


USD_SEK_SERIES_ID = "SEKUSDPMI"


def read_odata_values(path: Path) -> pd.DataFrame:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return pd.DataFrame(payload["value"])


def read_riksbank_rates() -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    for path in sorted(RAW_RIKSBANK_DIR.glob("exchange_rates_*.json")):
        year = int(path.stem.rsplit("_", 1)[1])
        payload = json.loads(path.read_text(encoding="utf-8"))
        observations = [row for row in payload if row["seriesId"] == USD_SEK_SERIES_ID]
        if not observations:
            raise ValueError(f"No {USD_SEK_SERIES_ID} observations found in {path}")

        latest = max(observations, key=lambda row: row["date"])
        rows.append(
            {
                "order_year": year,
                "series_id": USD_SEK_SERIES_ID,
                "rate_date": latest["date"],
                "exchange_rate_to_sek": float(latest["value"]),
            }
        )

    return pd.DataFrame(rows).sort_values("order_year").reset_index(drop=True)


def build_dim_date(order_dates: pd.Series) -> pd.DataFrame:
    dates = pd.date_range(order_dates.min(), order_dates.max(), freq="D")
    dim_date = pd.DataFrame({"date": dates.date})
    dim_date["year"] = dates.year
    dim_date["quarter"] = dates.quarter
    dim_date["month_number"] = dates.month
    dim_date["month_name"] = dates.strftime("%B")
    dim_date["year_month"] = dates.strftime("%Y-%m")
    return dim_date


def build_model_tables() -> dict[str, pd.DataFrame]:
    customers = read_odata_values(RAW_NORTHWIND_DIR / "customers.json")
    orders = read_odata_values(RAW_NORTHWIND_DIR / "orders.json")
    order_details = read_odata_values(RAW_NORTHWIND_DIR / "order_details.json")
    products = read_odata_values(RAW_NORTHWIND_DIR / "products.json")
    categories = read_odata_values(RAW_NORTHWIND_DIR / "categories.json")
    exchange_rates = read_riksbank_rates()

    orders["order_date"] = pd.to_datetime(orders["OrderDate"], utc=True).dt.date
    orders["order_year"] = pd.to_datetime(orders["OrderDate"], utc=True).dt.year

    fact_sales = (
        order_details.merge(
            orders[
                [
                    "OrderID",
                    "CustomerID",
                    "order_date",
                    "order_year",
                    "ShipCountry",
                    "ShipCity",
                ]
            ],
            on="OrderID",
            how="left",
        )
        .merge(products[["ProductID", "CategoryID"]], on="ProductID", how="left")
        .merge(exchange_rates, on="order_year", how="left")
    )

    fact_sales["line_amount"] = (
        fact_sales["UnitPrice"] * fact_sales["Quantity"] * (1 - fact_sales["Discount"])
    )
    fact_sales["line_amount_sek"] = fact_sales["line_amount"] * fact_sales["exchange_rate_to_sek"]
    fact_sales["order_detail_id"] = (
        fact_sales["OrderID"].astype(str) + "-" + fact_sales["ProductID"].astype(str)
    )

    fact_sales = fact_sales[
        [
            "order_detail_id",
            "OrderID",
            "CustomerID",
            "ProductID",
            "CategoryID",
            "order_date",
            "order_year",
            "ShipCountry",
            "ShipCity",
            "UnitPrice",
            "Quantity",
            "Discount",
            "line_amount",
            "exchange_rate_to_sek",
            "line_amount_sek",
        ]
    ].rename(
        columns={
            "OrderID": "order_id",
            "CustomerID": "customer_id",
            "ProductID": "product_id",
            "CategoryID": "category_id",
            "ShipCountry": "ship_country",
            "ShipCity": "ship_city",
            "UnitPrice": "unit_price",
            "Quantity": "quantity",
            "Discount": "discount",
        }
    )

    dim_customer = customers[
        ["CustomerID", "CompanyName", "ContactName", "City", "Region", "Country"]
    ].rename(
        columns={
            "CustomerID": "customer_id",
            "CompanyName": "company_name",
            "ContactName": "contact_name",
            "City": "city",
            "Region": "region",
            "Country": "country",
        }
    )

    dim_product = products[
        ["ProductID", "ProductName", "CategoryID", "QuantityPerUnit", "UnitPrice", "Discontinued"]
    ].rename(
        columns={
            "ProductID": "product_id",
            "ProductName": "product_name",
            "CategoryID": "category_id",
            "QuantityPerUnit": "quantity_per_unit",
            "UnitPrice": "list_unit_price",
            "Discontinued": "discontinued",
        }
    )

    dim_category = categories[["CategoryID", "CategoryName", "Description"]].rename(
        columns={
            "CategoryID": "category_id",
            "CategoryName": "category_name",
            "Description": "description",
        }
    )

    dim_date = build_dim_date(pd.to_datetime(orders["order_date"]))

    return {
        "fact_sales": fact_sales,
        "dim_customer": dim_customer,
        "dim_product": dim_product,
        "dim_category": dim_category,
        "dim_date": dim_date,
        "exchange_rates": exchange_rates,
    }