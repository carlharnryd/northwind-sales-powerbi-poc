# Architecture

The POC is designed as a local, reproducible analytical pipeline:

```text
Source APIs -> raw files -> DuckDB warehouse -> Power BI exports -> PBIX report
```

The implementation intentionally avoids cloud infrastructure, schedulers and
enterprise orchestration so the case can be reviewed and run from scratch on a
local machine.

## Implementation Notes

Northwind returns paginated OData responses for several entities. The pipeline
therefore follows `@odata.nextLink` until the full entity has been extracted.
This is necessary to avoid building the model from only the first page of data.

DuckDB is used as the local warehouse, and the report-facing model tables are
also exported as CSV files for simple Power BI ingestion.
