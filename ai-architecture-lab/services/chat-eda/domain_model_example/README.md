# Domain Model Example — chat-eda

This example demonstrates a small Domain Model with rich entities, unit tests for domain behavior, and a simple Data Mapper / Repository implemented with SQLite.

Purpose
- Show how domain objects encapsulate behavior (not just data).
- Provide a repository (data mapper) that persists domain objects to a relational store.
- Include unit tests for domain logic and integration tests for persistence.

Run tests

From the repository root run the example tests directly (this runs pytest in the example folder):

```powershell
cd ai-architecture-lab/services/chat-eda/domain_model_example
pytest -q
```

Notes
- The repository uses the built-in `sqlite3` module to avoid heavy external dependencies. The mapping is intentionally simple and educational.
