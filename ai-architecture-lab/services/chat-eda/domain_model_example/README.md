# Domain Model Example (Chat EDA)

Beginner-friendly demo of the Domain Model pattern: rich entities with behavior, persisted via a simple Data Mapper / Repository backed by SQLite.

## What you will learn
- How to keep business rules inside domain objects (`Conversation`, `Message`) instead of in routes/handlers.
- How a repository maps domain objects to a relational store (SQLite) without leaking SQL into the model.
- How to test domain behavior and persistence separately.

## Why Domain Model
- Use when logic grows beyond CRUD scripts and you need behaviorful objects (e.g., enforcing “no messages after close”).
- Keeps rules close to the data, making refactors and tests easier.
- Works well with ORMs or mappers; here we use lightweight `sqlite3` for clarity.

## Quick start (tests)
From the repo root:
```powershell
cd ai-architecture-lab/services/chat-eda/domain_model_example
python -m pytest -q
```

## Files to skim
- `app/domain.py` — Domain objects with behavior (add messages, close conversations, counts).
- `app/repository.py` — Data Mapper / Repository using SQLite tables for conversations and messages.
- `tests/test_domain.py` — Unit tests for the model behavior.
- `tests/test_repository.py` — Persistence tests for save/get/list flows.

## Real-world use cases
- Chat threads with rules (no posting to closed conversations, word-count limits).
- Support tickets with state transitions and audit history.
- Comment systems that need moderation rules before persistence.

## Notes
- Uses Python stdlib `sqlite3`; no external DB required.
- Repository recreates message rows on save for simplicity—good for teaching, not for high-scale use.
