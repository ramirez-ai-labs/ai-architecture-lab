# Transaction Script Example (Blog CMS)

This minimal example demonstrates the Transaction Script pattern for a Blog CMS: each HTTP request runs a small, procedural routine that performs the required CRUD operations.

Tech: Python 3.11+, FastAPI, Uvicorn, SQLite (builtin)

Run locally:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Endpoints:
- POST /posts -> create post
- GET /posts -> list posts
- GET /posts/{id} -> get post
- PUT /posts/{id} -> update post
- DELETE /posts/{id} -> delete post

This intentionally keeps domain logic inside request handlers (Transaction Script) for clarity.
