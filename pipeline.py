"""Orchestrator: extract -> validate -> transform -> load. Idempotent."""
import argparse, sqlite3
from datetime import date, timedelta

from quality import run_checks

DB = "warehouse.db"


def daterange(a: date, b: date):
    d = a
    while d <= b:
        yield d
        d += timedelta(days=1)


def ensure_schema(conn):
    conn.executescript(open("schema.sql").read())


def load_batch(conn, batch: date):
    """Simulated extract+transform+load for one date partition (idempotent)."""
    ds = batch.isoformat()
    conn.execute("INSERT OR IGNORE INTO dim_date VALUES (?,?,?,?,?,?)",
                 (int(ds.replace("-", "")), ds, batch.year, batch.month,
                  batch.day, batch.strftime("%A")))
    # ... extract from API, transform, upsert facts/dims ...
    conn.commit()
    run_checks(conn, ds)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", required=True)
    ap.add_argument("--until", required=True)
    ap.add_argument("--check-only", action="store_true")
    a = ap.parse_args()
    conn = sqlite3.connect(DB)
    ensure_schema(conn)
    since = date.fromisoformat(a.since)
    until = date.fromisoformat(a.until)
    for d in daterange(since, until):
        print(f"batch {d.isoformat()}")
        if not a.check_only:
            load_batch(conn, d)
    print("done")


if __name__ == "__main__":
    main()
