import duckdb

from src.config import POWERBI_DIR, WAREHOUSE_PATH
from src.extract import extract_all
from src.quality_checks import run_quality_checks
from src.transform import build_model_tables


POWERBI_EXPORT_TABLES = [
    "fact_sales",
    "dim_customer",
    "dim_product",
    "dim_category",
    "dim_date",
]


def write_warehouse(tables: dict[str, object]) -> None:
    WAREHOUSE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(WAREHOUSE_PATH)) as connection:
        for table_name, dataframe in tables.items():
            connection.register("df", dataframe)
            connection.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
            connection.unregister("df")


def export_powerbi_tables(tables: dict[str, object]) -> None:
    POWERBI_DIR.mkdir(parents=True, exist_ok=True)
    for table_name in POWERBI_EXPORT_TABLES:
        tables[table_name].to_csv(POWERBI_DIR / f"{table_name}.csv", index=False)


def main() -> None:
    extract_all()
    tables = build_model_tables()
    run_quality_checks(tables)
    write_warehouse(tables)
    export_powerbi_tables(tables)
    print(f"Warehouse written to {WAREHOUSE_PATH}")
    print(f"Power BI CSV files written to {POWERBI_DIR}")


if __name__ == "__main__":
    main()