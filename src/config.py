from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
RAW_NORTHWIND_DIR = RAW_DIR / "northwind"
RAW_RIKSBANK_DIR = RAW_DIR / "riksbank"
WAREHOUSE_DIR = DATA_DIR / "warehouse"
POWERBI_DIR = DATA_DIR / "powerbi"

NORTHWIND_BASE_URL = "https://services.odata.org/V4/Northwind/Northwind.svc"

NORTHWIND_ENTITIES = {
    "customers": "Customers",
    "orders": "Orders",
    "order_details": "Order_Details",
    "products": "Products",
    "categories": "Categories",
}

RIKSBANK_RATE_URLS = {
    1996: "https://api.riksbank.se/swea/v1/Observations/ByGroup/130/1996-12-25/1996-12-31",
    1997: "https://api.riksbank.se/swea/v1/Observations/ByGroup/130/1997-12-25/1997-12-31",
    1998: "https://api.riksbank.se/swea/v1/Observations/ByGroup/130/1998-12-25/1998-12-31",
}

WAREHOUSE_PATH = WAREHOUSE_DIR / "northwind.duckdb"