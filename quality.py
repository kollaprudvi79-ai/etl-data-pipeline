"""Data quality gates. Raises QualityError on failure."""
import sqlite3


class QualityError(Exception):
    pass


def run_checks(conn: sqlite3.Connection, batch_date: str):
    checks = [
        ("no_null_order_ids",
         "SELECT COUNT(*) FROM fact_orders WHERE order_id IS NULL", 0),
        ("positive_revenue",
         "SELECT COUNT(*) FROM fact_orders WHERE revenue < 0", 0),
        ("customer_fk_valid",
         """SELECT COUNT(*) FROM fact_orders f LEFT JOIN dim_customer c
            ON f.customer_sk = c.customer_sk WHERE c.customer_sk IS NULL""", 0),
        ("fresh_batch_present",
         f"SELECT COUNT(*) FROM fact_orders WHERE date_sk = "
         f"(SELECT date_sk FROM dim_date WHERE full_date = '{batch_date}')", None),
    ]
    for name, sql, expected in checks:
        got = conn.execute(sql).fetchone()[0]
        if expected is None:
            if got == 0:
                raise QualityError(f"[{name}] no rows for batch {batch_date}")
        elif got != expected:
            raise QualityError(f"[{name}] expected {expected}, got {got}")
        print(f"  ✓ {name}: {got}")
    print("all quality checks passed")
