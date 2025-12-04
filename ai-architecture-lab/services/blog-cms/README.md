# Blog CMS — Example Catalog

High-level index for the Blog CMS patterns. Each example has its own detailed README; use the links below to dive deeper.

## Examples
- `transaction_script_example/` — Transaction Script (FastAPI + SQLite); see `transaction_script_example/README.md` for walkthrough and commands.
- `active_record_example/` — Planned Active Record demo (TBD).
- `service_layer_example/` — Planned Service Layer demo (TBD).
- `domain_model_example/` — Planned Domain Model demo (TBD).
- More slots available for future patterns (e.g., Table Module, Repository).

## What this folder demonstrates
- How a simple blog/content system can be modeled with different PoEAA domain-logic patterns.
- A progression from request-level scripts to richer models and services as complexity grows.

## Tech (typical)
- Python 3.11+, FastAPI, SQLite (built-in) for the lightweight demos.
- Additional dependencies are listed per example in each subfolder’s `requirements.txt`.

## Docs
- `docs/architecture.md` — Architecture overview for blog-cms.
- `docs/sequence-diagram.md` — Request-flow sequence.
- `docs/adr/` — Architectural decisions.
