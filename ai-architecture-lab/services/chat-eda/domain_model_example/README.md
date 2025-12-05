# Domain Model Example (Chat EDA)

Beginner-friendly demo of the **Domain Model pattern**:  
rich Python entities with business behavior, persisted using a simple **Repository / Data Mapper** backed by SQLite.

This project is intentionally small but structured like real backend systems used in production.

---

## 🌱 What You Will Learn

- Why business rules belong **inside domain objects** (`Conversation`, `Message`)  
  and NOT inside API routes or SQL.
- How a **Repository** cleanly maps domain objects ⇄ SQLite tables  
  without leaking SQL into the model.
- How to **unit test domain logic** separately from the database.
- How to add a lightweight **FastAPI layer** on top of a domain model.

These ideas are the building blocks of scalable architectures used in AI systems, CRMs, financial platforms, and chat applications.

---

## 🧠 Why Domain Model? (Beginner Explanation)

Use the Domain Model pattern when:

- Logic grows beyond simple CRUD scripts  
- You need objects that **enforce rules**  
  (e.g., *“no messages allowed after a conversation is closed”*)
- You want clean, testable, maintainable code  
- You want to separate **business rules** from:
  - API frameworks  
  - persistence  
  - routing  
  - SQL queries  

### Benefits

✔ Rules live close to the data  
✔ Fewer bugs caused by duplicated logic  
✔ Tests are easier to write  
✔ The model can be reused by:
- CLIs  
- background jobs  
- AI/LLL pipelines  
- microservices  

### Architecture (Simple Diagram)
[ FastAPI / Presentation Layer ]
|
v
[ Domain Model (Behavior) ] <----> [ Repository (Persistence) ]
|
Contains rules:
- "cannot post if closed"
- message counts
- last-message logic

---

## 🚀 Quick Start (Running Tests)

From the repo root:

```powershell
cd ai-architecture-lab/services/chat-eda/domain_model_example
python -m pytest -q

```

Tests demonstrate:

- Domain behavior
- Repository persistence
- API integration

---

## 🌐 API Demo (Optional)

A small FastAPI wrapper shows how an application might use the Domain Model.

# Endpoints

| Method | Endpoint                       | Purpose                              |
| ------ | ------------------------------ | ------------------------------------ |
| POST   | `/conversations`               | Create a new conversation            |
| POST   | `/conversations/{id}/messages` | Add a message (domain rule enforced) |
| POST   | `/conversations/{id}/close`    | Close a conversation                 |
| GET    | `/conversations/{id}`          | Load a conversation and messages     |

# Run it locally

```bash
uvicorn app.api:app --reload --port 8001
```

Open the interactive API docs:

👉 http://localhost:8001/docs

---

### 📁 Files Worth Skimming

- app/domain.py
Domain classes (Conversation, Message) with behaviorful methods
(e.g., add_message, close, last_message, total_word_count)

- app/repository.py
Repository/Data Mapper that handles SQLite persistence without exposing SQL to the domain.

- app/api.py
Thin FastAPI wrapper that orchestrates domain + repository.

Tests

- tests/test_domain.py — Tests domain rules
- tests/test_repository.py — Tests persistence flow
- tests/test_api.py — Tests the HTTP layer

---

### 📌 Real-World Use Cases

The same pattern applies to many systems including:

🗨️ Chat Applications

- Enforcing conversation states
- Moderation rules
- Message validation

🎫 Support / Ticketing Systems

- Tickets with state transitions (open → in progress → closed)
- Audit history
- Agent actions

💬 Comment or Discussion Threads

- Preventing posts to locked threads
- Rate limiting or moderation rules

🤖 AI / LLM Pipelines

- Conversations as first-class objects
- Agent memory & context windows
- EDA-style traceable logs

Domain models make these features predictable, testable, and reusable.

---

📝 Notes & Teaching Tips

- Uses Python’s built-in sqlite3 — no external DB required.

- The Repository recreates all message rows on each save for simplicity.
(Great for teaching, not optimized for high-scale production.)

- The Domain Model has no FastAPI, no Pydantic, and no SQL,
making it portable to other applications or pipelines.
