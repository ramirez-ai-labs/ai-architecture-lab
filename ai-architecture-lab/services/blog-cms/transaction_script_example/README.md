# Transaction Script Example (Blog CMS)

This minimal example demonstrates the Transaction Script pattern for a Blog CMS: each HTTP request runs a small, procedural routine that performs the required CRUD operations.

Tech: Python 3.11+, FastAPI, Uvicorn, SQLite (builtin)

Run locally (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# start the server on port 8001 for this example
uvicorn app.main:app --reload --port 8001
```

Endpoints:
- POST /posts -> create post
- GET /posts -> list posts
- GET /posts/{id} -> get post
- PUT /posts/{id} -> update post
- DELETE /posts/{id} -> delete post

Notes and testing

- Database: by default the service writes to an on-disk SQLite file `./posts.db` (relative to the process working directory). The path can be overridden with the `DB_PATH` environment variable — useful for tests or running multiple instances:

	```powershell
	# example: run with a custom DB path
	$env:DB_PATH = "./tmp_posts.db" ; uvicorn app.main:app --reload --port 8001
	```

- `posts.db` is included in the example `.gitignore`, so local DB files are not committed.

- Tests: the included pytest tests isolate the DB by setting `DB_PATH` to a temporary file and reloading the module. To run tests:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
```

- DTOs: the example exposes simple request/response DTOs (`PostIn` and `PostOut`) using Pydantic. The handlers are intentionally procedural (Transaction Scripts) and return DTOs directly.

This intentionally keeps domain logic inside request handlers (Transaction Script) for clarity.
