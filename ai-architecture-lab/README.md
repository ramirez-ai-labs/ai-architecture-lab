# AI Architecture Lab

Monorepo showcasing architecture patterns and example services for learning and experimentation.

Structure overview:

- docs/: global docs and diagrams
- common/: shared configs and libraries
- services/: example services demonstrating different architectures
- scripts/: helper scripts for setup, testing, and linting

See the `docs/architecture-overview.md` for a high-level explanation.

## Setup

Prerequisites — install these free tools locally before you start:

- Python (for FastAPI projects) and/or Node.js (for Express projects)
- SQLite (simple local relational database)
- Docker Desktop (Community Edition) for containers and compose
- RabbitMQ or Redis (for local event-driven testing)
- Git and GitHub (version control and remote hosting)
- Optional: Mermaid.js for rendering diagrams in README files

Goal: Have the tools installed and verified by running a small "Hello World" project for each tech (example: a FastAPI app and a small Express app that both respond to HTTP /health).

Service docs quick links:

- Blog CMS: `services/blog-cms/docs/architecture.md`
- Ecommerce: `services/ecommerce-microservices/docs/architecture.md`
- Chat EDA: `services/chat-eda/docs/architecture.md`
- Bank CQRS: `services/bank-cqrs/docs/architecture.md`
