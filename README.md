# Data Engineering Assessment

**Estimated time:** 2–2.5 hours  
**Submission:** Push your completed work to the provided GitHub repo (or zip and email)

---

## Context

You are joining a team that builds and maintains a data platform for an e-commerce business.
This repo contains raw CSV data and a set of transformation tasks that model that data into
an analytics-ready layer.

**Use whatever tool you are most comfortable with.** Common choices include:

- SQL scripts (SQLite, DuckDB, PostgreSQL, BigQuery, Snowflake, etc.)
- Python (pandas, polars, DuckDB Python API)
- A transformation framework (dbt, SQLMesh, etc.)

We are reviewing your code directly — **no running data warehouse or orchestration platform
is required**. Correct, readable code is what we are after.

---

## The data

Two CSV files are provided in `data/`:

| File | Description |
|------|-------------|
| `data/raw_orders.csv` | 15 order rows. Columns: `order_id`, `customer_id`, `order_date`, `status`, `amount_usd`, `country_code` |
| `data/raw_customers.csv` | 9 customer rows. Columns: `customer_id`, `first_name`, `last_name`, `email`, `signup_date`, `tier` |

---

## Tasks

### Task 1 — Staging / cleaning layer

Produce two cleaned datasets from the raw CSVs. You can output these as SQL views, CTEs,
DataFrames, new CSV files, or any other intermediate form — as long as the logic is clear.

#### 1a — Clean orders (`stg_orders`)

Starting from `raw_orders`:

1. Rename `amount_usd` → `order_amount`.
2. Normalise `status` to lowercase.
3. Cast `order_date` to a date type.
4. **Exclude** any row where `order_amount` is `NULL` or `0`.
5. Add a column `loaded_at` recording when the row was processed (current timestamp).

#### 1b — Clean customers (`stg_customers`)

Starting from `raw_customers`:

1. Combine `first_name` and `last_name` into a single `full_name` column.
2. Keep all other columns as-is.
3. Add a column `loaded_at` recording when the row was processed.

**What we are looking for:**
- Correct identification and handling of bad/null data before it propagates downstream
- Clean, readable transformations
- Sensible column naming

---

### Task 2 — Enrichment and aggregation

#### 2a — Enriched orders (`int_orders_enriched`)

Join your cleaned orders to your cleaned customers on `customer_id`. Keep:

- `order_id`, `customer_id`, `full_name`, `tier`, `order_date`, `status`, `order_amount`, `country_code`
- A boolean column `is_completed` that is `TRUE` when `status = 'completed'`

Only include orders where `status` is `'completed'` or `'pending'`.

#### 2b — Customer summary (`customer_orders`)

Aggregate `int_orders_enriched` to one row per customer. Produce:

| Column | Definition |
|--------|------------|
| `customer_id` | |
| `full_name` | |
| `tier` | |
| `total_orders` | Count of all orders for this customer |
| `completed_orders` | Count of orders where `is_completed = TRUE` |
| `total_revenue` | Sum of `order_amount` for completed orders only |
| `avg_order_value` | Average `order_amount` for completed orders, rounded to 2 decimal places |
| `first_order_date` | Earliest `order_date` |
| `last_order_date` | Most recent `order_date` |

Only include customers who have at least one completed order.

**What we are looking for:**
- Correct join type and logic
- Accurate aggregations that distinguish completed orders from all orders
- Awareness of which rows to include vs. exclude

---

### Task 3 — Data quality checks

Write checks that validate the following assertions. These can be SQL queries, Python
assertions, unit tests, or dbt/SQLMesh tests — whatever fits your chosen tool.

| # | Dataset | Assertion |
|---|---------|-----------|
| 1 | `stg_orders` | `order_id` is unique and never null |
| 2 | `stg_orders` | `customer_id` is never null |
| 3 | `stg_orders` | `status` is always one of: `completed`, `pending`, `cancelled`, `refunded` |
| 4 | `stg_orders` | `order_amount` is never null |
| 5 | `customer_orders` | `customer_id` is unique and never null |
| 6 | `customer_orders` | `total_revenue` is never null |
| 7 | `customer_orders` | No customer has a `total_revenue` of 0 or less |

For each check, the important thing is that a violation produces a clear, visible failure
(a thrown exception, a non-empty result set, a failed assertion, etc.).

**What we are looking for:**
- Correct identification of what to test and why
- Checks that would actually catch a regression if the data changed
- Clarity — it should be obvious what each check is asserting

---

### Task 4 — Orchestration

Describe (in code or pseudocode) how you would schedule and run this pipeline automatically.

Requirements:
- Runs daily at 06:00 UTC
- Steps run in order: load raw data → transform → run quality checks → notify on success
- If the quality checks fail, the success notification must **not** run
- At least one retry on transient failure
- Owner / contact is identifiable

You may write this as:
- An Airflow DAG
- A Prefect flow
- A GitHub Actions workflow
- A shell/Python script with scheduling comments
- Or any other orchestration approach you know

The code does not need to be executable — we are reviewing your design thinking.

**What we are looking for:**
- Correct step ordering and dependency modelling
- Appropriate handling of failure (no false-positive success notifications)
- Clean, readable code — not a copy from documentation

---

### Stretch task (optional)

Inspect `data/raw_orders.csv` carefully.  
There are **three data quality issues** intentionally seeded into the file.

Document your findings — either in a new file `FINDINGS.md` or as a comment at the top of
your data quality checks file:

- What is each issue?
- Why is it a problem for the pipeline?
- How does your pipeline currently handle it (or how should it)?

---

## Repo structure

```
de-test/
├── data/
│   ├── raw_orders.csv         ← raw order data (Task 1a source)
│   └── raw_customers.csv      ← raw customer data (Task 1b source)
├── transforms/
│   ├── stg_orders.*           ← Task 1a  (create or rename as appropriate)
│   ├── stg_customers.*        ← Task 1b
│   ├── int_orders_enriched.*  ← Task 2a
│   └── customer_orders.*      ← Task 2b
├── quality/
│   └── checks.*               ← Task 3  (create or rename as appropriate)
├── orchestration/
│   └── pipeline.*             ← Task 4  (create or rename as appropriate)
└── FINDINGS.md                ← Stretch task (optional)
```

You are not required to follow this structure exactly. Organise your work in whatever way
makes sense for your chosen tool. If your tool has its own conventional layout (e.g. dbt's
`models/` directory), use that instead.

> **Note:** You may also notice `models/`, `tests/`, `dags/`, `seeds/`, and `dbt_project.yml`
> in the repo root. These are dbt scaffolding files included for candidates who choose to use
> dbt. If you are not using dbt, you can ignore them.

---

## Submission checklist

- [ ] `stg_orders` — cleaning logic implemented
- [ ] `stg_customers` — cleaning logic implemented
- [ ] `int_orders_enriched` — enrichment logic implemented
- [ ] `customer_orders` — aggregation logic implemented
- [ ] Data quality checks written (assertions 1–7)
- [ ] Orchestration described (Task 4)
- [ ] (Optional) Stretch findings documented

---

## Notes

- Add brief comments explaining any deliberate trade-offs or assumptions.
- You are welcome to add additional intermediate steps or helper files.
- You do **not** need to produce final output CSVs or load data anywhere — the transformation
  logic is what we are reviewing.
