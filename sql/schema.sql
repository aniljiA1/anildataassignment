-- sql/schema.sql
-- DDL for trade_clean (Postgres style). Adjust types for other DBs.

CREATE TABLE IF NOT EXISTS trade_clean (
  id SERIAL PRIMARY KEY,
  date DATE,
  year INT,
  month INT,
  hsn_code VARCHAR(64),
  hsn_description TEXT,
  goods_description TEXT,
  raw_description TEXT,
  model_name VARCHAR(256),
  model_number VARCHAR(256),
  capacity_spec VARCHAR(128),
  material VARCHAR(64),
  embedded_quantity INT,
  unit VARCHAR(32),
  unit_standard VARCHAR(32),
  unit_price_inr NUMERIC(18,4),
  total_value_inr NUMERIC(18,2),
  duty_paid_inr NUMERIC(18,2),
  grand_total_inr NUMERIC(18,2),
  quantity_num NUMERIC(18,4),
  landed_cost_per_unit NUMERIC(18,4),
  supplier_name TEXT,
  supplier_address TEXT,
  parsing_confidence NUMERIC(5,2),
  parsing_pass BOOLEAN
);

-- Indexes to speed queries
CREATE INDEX IF NOT EXISTS idx_trade_year ON trade_clean(year);
CREATE INDEX IF NOT EXISTS idx_trade_hsn ON trade_clean(hsn_code);
CREATE INDEX IF NOT EXISTS idx_trade_model ON trade_clean(model_number);
CREATE INDEX IF NOT EXISTS idx_trade_supplier ON trade_clean(supplier_name);
