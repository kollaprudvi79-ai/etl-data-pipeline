-- Star schema for e-commerce orders
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT NOT NULL,
    name TEXT, email TEXT, region TEXT,
    valid_from DATE NOT NULL, valid_to DATE,
    is_current INTEGER DEFAULT 1,
    UNIQUE(customer_id, valid_from)
);
CREATE TABLE IF NOT EXISTS dim_product (
    product_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT UNIQUE NOT NULL,
    name TEXT, category TEXT, unit_price REAL
);
CREATE TABLE IF NOT EXISTS dim_date (
    date_sk INTEGER PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    year INTEGER, month INTEGER, day INTEGER, weekday TEXT
);
CREATE TABLE IF NOT EXISTS fact_orders (
    order_id TEXT PRIMARY KEY,
    customer_sk INTEGER REFERENCES dim_customer(customer_sk),
    product_sk INTEGER REFERENCES dim_product(product_sk),
    date_sk INTEGER REFERENCES dim_date(date_sk),
    qty INTEGER NOT NULL CHECK (qty > 0),
    revenue REAL NOT NULL CHECK (revenue >= 0),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS pipeline_state (
    key TEXT PRIMARY KEY, value TEXT
);
