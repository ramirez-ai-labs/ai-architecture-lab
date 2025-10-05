# Bank CQRS Architecture

This service demonstrates CQRS (Command Query Responsibility Segregation) with event sourcing. Components:

- command-service: handles writes, validates commands, emits events
- event-store: durable append-only store of events
- query-service: materializes read models from events for fast queries

Operational notes:
- Use immutable events with versioning
- Ensure idempotency and deduplication at the event consumer
- Provide snapshots for large aggregates

See `adr/` for design decisions.
