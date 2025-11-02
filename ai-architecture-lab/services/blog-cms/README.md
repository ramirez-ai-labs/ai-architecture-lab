# Blog CMS — Examples & Notes

Summary
-------
This folder contains examples and documentation for a tiny Blog CMS used in the lab. The primary example demonstrates the Transaction Script pattern (see `transaction_script_example/`). Use this folder as a place to add additional blog-related examples or refactor the existing example into other patterns.

What this demonstrates
----------------------
- Transaction Script pattern (in `transaction_script_example/`) — handlers that perform database operations directly.
- How to move from simple request-level scripts to Service/Repository structures (future examples).

Tech
----
- Python 3.11+, FastAPI, SQLite (builtin)

Pattern examples
----------------
- `transaction_script_example/` — Transaction Script pattern: procedural HTTP handlers executing SQL statements. See `transaction_script_example/README.md` for run and test instructions.
- (Planned) `active_record_example/` — Active Record style models with `.save()` semantics (not implemented yet).

Quick start
-----------
Run the included example (Transaction Script) from the example folder. Two common flows are shown below.

PowerShell (Windows):

```powershell
cd ai-architecture-lab/services/blog-cms/transaction_script_example
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Bash (macOS / Linux):

```bash
cd ai-architecture-lab/services/blog-cms/transaction_script_example
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Notes for learners
------------------
- The transaction script example keeps domain logic inside HTTP handlers so each handler is an explicit procedure: open DB, run SQL, commit, return DTO.
- To show alternatives (Domain Model, Active Record, Service Layer), add sibling example folders following the same pattern and include a README describing the pattern and how to run tests.

Tests
-----
From the example folder run:

```powershell
pytest -q
```

Docs
----
- `docs/architecture.md` — architecture overview for the blog-cms service
- `docs/sequence-diagram.md` — sequence diagram for request flows
- `docs/adr/` — architectural decisions
<<<<<<< HEAD
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
=======
# Blog CMS

Small CMS used in examples for presentation of several PoEAA patterns.

Overview
--------
This service is used to demonstrate presentation and persistence patterns for a blog/content system.

Pattern examples
----------------
- `transaction_script_example/` — Transaction Script pattern: procedural HTTP handlers that perform SQL statements directly. (See `transaction_script_example/README.md` for how to run and test.)
- (Planned) `active_record_example/` — Active Record style models with `.save()` semantics (not implemented yet).

Docs
----
- `docs/architecture.md` — architecture overview for the blog-cms service
- `docs/sequence-diagram.md` — sequence diagram for request flows
- `docs/adr/` — architectural decisions

How to run examples
-------------------
Each example includes a README with commands. Example (transaction script):

```powershell
cd ai-architecture-lab/services/blog-cms/transaction_script_example
pytest -q
```

Want me to scaffold an `active_record_example` here? I can add a small Peewee-based demo with tests.
>>>>>>> c2adc14 (docs(services): normalize service READMEs and add blog-cms README)
