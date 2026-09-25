# Northwind Sales Power BI POC

This repository contains a standalone proof of concept for a data engineering case.
It extracts sales data from the public Northwind OData API, enriches it with yearly
exchange rates from the Riksbank API, builds a small local analytical model, and
supports a Power BI report showing sales in SEK.

## Current Status

Initial project scaffold. The next implementation step is to inspect the API
responses and then implement the extract and transform pipeline.

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
python -m src.build_warehouse
```

## Documentation

- [docs/architecture.md](docs/architecture.md)
- [docs/assumptions.md](docs/assumptions.md)
- [docs/data_model.md](docs/data_model.md)
- [docs/ai_usage.md](docs/ai_usage.md)
