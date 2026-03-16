"""
Task 4 — Orchestration

Describe how you would schedule and run this pipeline automatically.

Requirements
------------
1. Runs daily at 06:00 UTC.
2. Steps run in order:
     a. load_data       — make the raw CSV data available (seed, ingest, copy, etc.)
     b. transform       — run all transformation steps (Tasks 1 and 2)
     c. quality_checks  — run all data quality checks (Task 3)
     d. notify_success  — log or send a "Pipeline complete" notification
3. If quality_checks fails, notify_success must NOT run.
4. At least one retry on transient failure.
5. Owner / contact is identifiable from the code.

You may implement this as:
  - An Airflow DAG
  - A Prefect flow
  - A GitHub Actions workflow
  - A shell or Python script with scheduling comments
  - Or any other orchestration approach you know

The code does not need to be executable against a live system.
We are reviewing your design thinking and your ability to model dependencies correctly.

YOUR IMPLEMENTATION BELOW
"""
