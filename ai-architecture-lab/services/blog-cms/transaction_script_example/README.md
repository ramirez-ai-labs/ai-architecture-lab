# Beginner Guide: Transaction Script Pattern (Tiny Blog CMS)
===========================================================

This project demonstrates a **very simple Blog CMS** using the  
**Transaction Script** pattern with FastAPI + SQLite.

It is intentionally minimal so **new developers** can clearly follow how an HTTP request becomes a database operation and returns a response.

---

## 🌱 What Is the Transaction Script Pattern?

In this pattern, **each API endpoint contains all the steps needed** to complete a business operation.

Example: `POST /posts` does everything:

1. Receives input (title + content)  
2. Opens the database  
3. Inserts a new row  
4. Saves (commits) the change  
5. Sends back the created post as JSON  

There are **no extra layers**, no ORM, no services — just clear, linear logic.

This simplicity makes it ideal for learning CRUD and web backend fundamentals.

---

## 🎓 What You Will Learn

- How FastAPI routes work  
- How to validate input/output using **Pydantic**  
- How to use **SQLite**, a small file-based database  
- How endpoint logic maps directly to SQL statements  
- Why Transaction Script is a great beginner pattern  
- How to override the database file using the `DB_PATH` environment variable  
  (important for tests and isolation)

---

## 🌟 Why This Example Helps Beginners

- SQLite requires **no setup** — it's just a file on disk.  
- Each endpoint shows the full flow of a request → SQL → response.  
- No advanced architecture or abstractions.  
- Easier to read than examples using ORMs or service layers.  

It's the perfect stepping stone before learning:
- SQLAlchemy
- Service Layer pattern
- Repository pattern
- Domain-driven design (DDD)

---

## 📦 Project Structure
```bash
app/
└── main.py # All routes + database helper functions
```

A small structure on purpose — easier learning!

---

## 🧭 How a Request Flows (Beginner Diagram)

Example: `GET /posts/1`

```mermaid
flowchart TD
  A[Client request: GET /posts/1] --> B[FastAPI route: get_post]
  B --> C[Open SQLite database file]
  C --> D[Run SQL: SELECT * FROM posts WHERE id = 1]
  D --> E[Convert row to Pydantic model (PostOut)]
  E --> F[Return JSON response]
```

Every operation is easy to trace because the logic stays in one place.

---

## 🛠️ Tech Used

- **Python 3.11+**  
- **FastAPI** (web framework)  
- **Uvicorn** (server)  
- **SQLite** (built into Python)  
- **Pydantic** (validation)

No external database or infrastructure required.

---

## 🚀 Quick Start (macOS / zsh)

Run the example from the repo root:

```bash
cd ai-architecture-lab/services/blog-cms/transaction_script_example
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open Swagger UI:

👉 http://localhost:8000/docs

---

## 🧰 Environment Variable: DB_PATH

SQLite stores data in one file (default: ./posts.db).

You can change which DB file is used:
```bash
export DB_PATH=./my_temp_db.db
```

This is especially helpful when:

- running tests
- isolating different environments
- experimenting safely

---

## 🔗 HTTP Endpoints

| Method | Endpoint      | Description    |
|--------|---------------|----------------|
| POST   | /posts        | Create a post  |
| GET    | /posts        | List all posts |
| GET    | /posts/{id}   | Get one post   |
| PUT    | /posts/{id}   | Update a post  |
| DELETE | /posts/{id}   | Delete a post  |

Each route is a complete transaction script:
open DB → run SQL → commit (if needed) → return response.

---

## 🧪 Running Tests

Install test dependencies and run:
```bash
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest -q
```

Tests automatically:

- Create a temporary SQLite DB
- Override DB_PATH
- Reload the module
- Run isolated CRUD tests safely

Your local posts.db is never touched.

---

## 🧠 Notes for Learners

You are seeing raw SQL — this is great for learning.

Pydantic ensures your API receives and returns clean data.

FastAPI automatically generates interactive docs.

SQLite keeps storage simple and visible.

This pattern is commonly used for:

- Internal tools
- Admin dashboards
- Small microservices
- Hackathon projects
- Teaching backend fundamentals
