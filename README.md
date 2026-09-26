# Northwind Sales Power BI POC

This repository contains a standalone proof of concept for a data engineering case.
It extracts sales data from the public Northwind OData API, enriches it with yearly
exchange rates from the Riksbank API, builds a small local analytical model, and
supports a Power BI report showing sales in SEK.

## Current Status

The extract, transform, local warehouse build and Power BI CSV export are
implemented. The next step is to connect Power BI Desktop to the exported CSV
tables and build the report pages.

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

## Planned Run Command

```powershell
.\.venv\Scripts\python.exe -m src.build_warehouse
```

The command writes:

- raw API payloads to `data/raw/`
- a DuckDB database to `data/warehouse/northwind.duckdb`
- Power BI import files to `data/powerbi/`

Generated data folders are ignored by Git because they can be rebuilt from the
public APIs.

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
