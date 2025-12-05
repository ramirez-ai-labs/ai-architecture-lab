# Chat EDA — Example Catalog

High-level index for the chat event-driven and domain model examples. Each example has its own detailed README; use the links below to dive deeper.

## Examples
- `domain_model_example/` — Domain Model: rich entities (`Conversation`, `Message`) plus a simple Data Mapper / Repository. See `domain_model_example/README.md` for walkthrough and test commands.
- `orm_patterns/` — Planned object-relational behavioral patterns (Unit of Work, Identity Map), not yet implemented.
- Additional slots available for broker-focused demos (publish/subscribe, event handlers).

## What this folder demonstrates
- How to model a chat domain with behaviorful entities and persist them via a mapper/repository.
- How event-driven components (broker placeholders) can sit alongside domain logic in a small lab.

## Tech (typical)
- Python for examples, SQLite for lightweight persistence in the domain model sample.
- Broker concepts (Kafka/RabbitMQ) for future event-driven demos.

## Docs
- `docs/architecture.md` — architecture overview for chat-eda.
