# E-Commerce ETL Pipeline — Data Engineer Project

> **Problem:** An e-commerce company pulls order data from 3 different APIs. Each returns different formats, has missing fields, duplicate records, and occasional schema changes. Revenue reports differ by 15% depending on who queries.

> **Solution:** Production-grade batch ETL with bronze/silver/gold medallion architecture, 12 automated data quality gates, and idempotent loads. Every number traceable, every failure loud.

**Live case study:** https://kollaprudvi79-ai.github.io/etl-data-pipeline/

## 📊 Business Impact

| Before | After |
|--------|-------|
| Reports differ by 15% | Single source of truth, 0% variance |
| Manual CSV uploads, 4 hrs/day | Automated, 15 min runtime |
| Silent data corruption | 12 quality gates, fails loudly |
| No backfill | Any date range reprocessable |

## 🏗️ Architecture

```
API (extract) → Bronze (raw JSON) → Silver (validated) → Gold (star schema)
                                        ↓
                                  Quality Gates
```

- **Bronze:** Immutable raw landing — replayable if upstream breaks
- **Silver:** Cleaned, typed, deduplicated, SCD Type 2 for customers
- **Gold:** Star schema (`fact_orders`, `dim_customer`, `dim_product`, `dim_date`)

## 🔧 Key Decisions
1. **Idempotent upserts** — re-runs produce identical results, zero duplicates
2. **SCD Type 2** — customer history preserved for compliance
3. **Quality gates** — null/range/FK/freshness checks block bad loads
4. **Watermark** — restarts resume from failure, not from scratch

## 🚀 Quickstart
```bash
python pipeline.py --since 2025-01-01 --until 2025-01-31
python pipeline.py --check-only
```

## 🛠️ Stack
`Python` `PostgreSQL` `Docker` `SQL`
