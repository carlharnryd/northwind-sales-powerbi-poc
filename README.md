# Northwind Sales Power BI POC

This repository contains a standalone proof of concept for a data engineering case.
It extracts sales data from the public Northwind OData API, enriches it with yearly
exchange rates from the Riksbank API, builds a small local analytical model, and
supports a Power BI report showing sales in SEK.

## Current Status

The extract, transform, local warehouse build and Power BI CSV export are
implemented. The Power BI report is also built and stored at
`powerbi/northwind_sales_report.pbix`.

The report uses imported data. This means the saved `.pbix` file contains the
data needed to open and present the report, while refreshing the report from
source requires the report CSV files to exist at the local paths used when the
report was built. The five report CSV files are included in the repository so
the delivered project contains a ready-to-use Power BI data layer.

## Planned Architecture

```text
Northwind API + Riksbank API
  -> raw JSON files
  -> DuckDB local warehouse
  -> exported Power BI tables
  -> Power BI report (.pbix)
```

## Tools

- Python for extraction, transformation and loading.
- DuckDB as a local analytical database.
- CSV exports for simple Power BI ingestion.
- Power BI Desktop for the report file.

## Local Setup

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Rebuild the Data Locally

```powershell
.\.venv\Scripts\python.exe -m src.build_warehouse
```

The command writes:

- raw API payloads to `data/raw/`
- a DuckDB database to `data/warehouse/northwind.duckdb`
- Power BI import files to `data/powerbi/`

Raw API payloads and the local warehouse are ignored by Git because they can be
rebuilt from the public APIs. The Power BI CSV exports are tracked in Git so a
fresh clone contains the data layer used by the delivered report.

## Start from a Fresh Clone

1. Clone the repository and open the repository folder in VS Code.
2. Confirm that Python and Power BI Desktop are installed.
3. Create the virtual environment and install the packages using the commands
   in **Local Setup**.
4. Run `.\.venv\Scripts\python.exe -m src.build_warehouse` from the repository
    root. This downloads the raw API data, creates the DuckDB warehouse and
    writes the five CSV files under `data/powerbi/`.
5. Open `powerbi/northwind_sales_report.pbix` in Power BI Desktop to view the
  delivered report.
6. If you want to refresh the report from the CSV files, use **Refresh** in
  Power BI Desktop. To refresh from a newly cloned copy, the report must be
  opened from the same local repository path used when it was created, or the
  CSV data-source paths must be updated in Power Query.

Opening the `.pbix` file and viewing its imported data does not require the
Python environment to be active. Rebuilding or refreshing the source data does.

## Repository Contents and Data Delivery

Tracked in Git:

- Python source code and configuration.
- Documentation and validation results.
- `powerbi/northwind_sales_report.pbix`, the delivered report.

Tracked in Git and used by the Power BI report:

- `data/powerbi/fact_sales.csv`, the sales fact export.
- `data/powerbi/dim_customer.csv`, the customer dimension export.
- `data/powerbi/dim_product.csv`, the product dimension export.
- `data/powerbi/dim_category.csv`, the category dimension export.
- `data/powerbi/dim_date.csv`, the date dimension export.

Generated locally and intentionally ignored by Git:

- `data/raw/`, downloaded JSON payloads.
- `data/warehouse/`, the local DuckDB database.
The generated data is reproducible from the public Northwind OData API and the
Riksbank API. The source values, row counts and validation totals are recorded
in [docs/data_profile.md](docs/data_profile.md). The main limitation is that
the APIs must be reachable when rebuilding or refreshing the data.

## Current Validation Snapshot

Latest local validation produced:

- `fact_sales`: 2,155 rows
- distinct orders: 830
- total sales: 9,839,628.90 SEK
- USD/SEK rates: 1996 = 6.870, 1997 = 7.870, 1998 = 8.065

## Documentation

- [docs/architecture.md](docs/architecture.md)
- [docs/assumptions.md](docs/assumptions.md)
- [docs/data_model.md](docs/data_model.md)
- [docs/ai_usage.md](docs/ai_usage.md)
- [docs/powerbi_desktop_guide.md](docs/powerbi_desktop_guide.md)
