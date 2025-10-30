# Transaction Script Example (Blog CMS)

Summary
-------
Small, self-contained example showing the Transaction Script pattern: each HTTP handler is a short procedural routine that performs the necessary CRUD operations.

What this demonstrates
----------------------
- Transaction Script pattern (logic inside request handlers)
- Simple DTOs with Pydantic
- Using SQLite for a tiny, local persistence layer

Tech
----
- Python 3.11+, FastAPI, Uvicorn, SQLite (builtin)

Quick start (macOS / zsh)
------------------------
Run the example locally from the repo root:

```bash
cd ai-architecture-lab/services/blog-cms/transaction_script_example
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

HTTP endpoints
--------------
- POST   /posts         — create post
- GET    /posts         — list posts
- GET    /posts/{id}    — get post
- PUT    /posts/{id}    — update post
- DELETE /posts/{id}    — delete post

Notes for learners
------------------
- This example keeps domain logic in handlers (Transaction Scripts) to make the request flow obvious and easy to debug.
- The `DB_PATH` environment variable controls the SQLite file path (default: `./posts.db`). Tests override `DB_PATH` and reload the module to get an isolated DB.

Tests
-----
Install dev deps and run pytest from the example folder:

```bash
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest -q
```

The tests use a temporary DB file per test run so examples can be run without affecting your local dev DB.
