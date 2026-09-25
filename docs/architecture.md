# Architecture

The POC is designed as a local, reproducible analytical pipeline:

```text
Source APIs -> raw files -> DuckDB warehouse -> Power BI exports -> PBIX report
```

The implementation intentionally avoids cloud infrastructure, schedulers and
enterprise orchestration so the case can be reviewed and run from scratch on a
local machine.
