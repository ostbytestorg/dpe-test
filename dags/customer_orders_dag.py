"""
Task 4 — Orchestration  (Airflow scaffold)

If you are using Airflow, implement your DAG here.
If you are using a different orchestration tool, implement in orchestration/pipeline.py
(or a file of your choosing) and ignore or delete this file.

Requirements
------------
1. Runs daily at 06:00 UTC.
2. Steps run in order:
     a. load_data       — make the raw CSV data available
     b. transform       — run all transformation steps (Tasks 1 and 2)
     c. quality_checks  — run all data quality checks (Task 3)
     d. notify_success  — log or send a "Pipeline complete" notification
3. If quality_checks fails, notify_success must NOT run.
4. At least one retry on transient failure.
5. Owner / contact is identifiable from the code.

You do NOT need a running Airflow instance. Correct, readable Python code is sufficient.
"""

# Your Airflow imports and implementation below
