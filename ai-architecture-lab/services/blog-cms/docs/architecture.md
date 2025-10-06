# Blog CMS Architecture

This document describes the layered architecture used by the Blog CMS service: presentation, application, domain, and infrastructure layers.

### Layers

- Presentation — controllers, HTTP/GraphQL adapters, request/response models
- Application — use cases, DTOs, application services
- Domain — entities, value objects, domain services, repository interfaces
- Infrastructure — repository implementations, external integrations, notifications, plugins

### Tech choices

- Language: Python (FastAPI) or Node.js (Express)
- Persistence: SQLite for local demos (replaceable with a real DB for production)

### Trade-offs

- Pros: clear separation of concerns, testability, easy to reason about domain logic
- Cons: more boilerplate; eventual consistency for async flows
