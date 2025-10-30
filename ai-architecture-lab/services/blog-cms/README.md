# Blog CMS — Examples & Notes

Summary
-------
This folder contains examples and documentation for a tiny Blog CMS used in the lab. The primary example demonstrates the Transaction Script pattern (see `transaction_script_example/`). Use this folder as a place to add additional blog-related examples or refactor the existing example into other patterns.

What this demonstrates
----------------------
- Transaction Script pattern (in `transaction_script_example`)
- How to move from simple request-level scripts to a service/repository structure

Tech
----
- Python 3.11+, FastAPI, SQLite (builtin)

Quick start
-----------
Run the included example (Transaction Script) from the repo root:

```bash
cd ai-architecture-lab/services/blog-cms/transaction_script_example
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --reload --port 8000
```

Notes for learners
------------------
- The transaction script example keeps domain logic inside HTTP handlers so each handler is an explicit procedure: open DB, run SQL, commit, return DTO.
- If you want to add Service Layer examples, consider creating a sibling folder (e.g., `service_layer_example/`) following the `bank-cqrs/simple_cqrs` structure.

Tests
-----
Run tests for the example (from the example folder):

```bash
source .venv/bin/activate
PYTHONPATH=. pytest -q
```
