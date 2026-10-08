# E-Commerce ETL Pipeline — Data Engineer Project

Batch ETL pipeline: extract raw orders from a REST API → validate & transform → load into a star-schema warehouse (SQLite/Postgres). Includes data-quality checks, idempotent loads, and backfill support.

**Docs / architecture:** https://kollaprudvi79-ai.github.io/etl-data-pipeline/

## Architecture

```
API (extract) → Bronze (raw JSON) → Silver (validated, typed) → Gold (star schema)
                                                      ↓
                                              Great-Expectations-style checks
```

## Features
- **Idempotent** loads via natural-key upserts — safe re-runs
- **Data quality gates**: null checks, range checks, referential integrity, freshness SLA
- **Slowly Changing Dimension Type 2** for customer records
- **Backfill** any date range with `--since/--until`
- Partitioned by event date; incremental watermark stored in `pipeline_state`

## Quickstart
```bash
pip install -r requirements.txt
python pipeline.py --since 2025-01-01 --until 2025-01-31
python pipeline.py --check-only   # run quality checks without loading
```

## Layout
- `pipeline.py` — orchestrator (extract → validate → transform → load)
- `extract.py` — paginated API client with retries/backoff
- `transform.py` — bronze→silver→gold, SCD2 logic
- `quality.py` — configurable check suite, fails loudly
- `schema.sql` — warehouse DDL (star schema)
- `Dockerfile` / `docker-compose.yml` — reproducible runs
