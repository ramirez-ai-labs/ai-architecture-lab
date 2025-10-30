# Ecommerce Microservices — Collection

Summary
-------
Collection of small microservices that form a simple e-commerce example. This folder includes a `docker-compose.yml` to run the services locally for demonstration and integration testing.

What this demonstrates
----------------------
- Microservice decomposition (API gateway, inventory, orders, payments)
- Local integration via Docker Compose
- Patterns like Remote Facade, Gateway, and message-based communication (docs/architecture.md)

Tech
----
- Docker Compose, Python/HTTP services, and optional message broker for async flows

Quick start
-----------
From the `ecommerce-microservices` folder you can bring up the example with:

```bash
cd ai-architecture-lab/services/ecommerce-microservices
docker compose up --build
```

Notes for learners
------------------
- The `services/` subfolder shows the individual microservice placeholders. Each service can be implemented independently for experiments.
- See `docs/architecture.md` for design notes and patterns used in this example.

If you want, I can scaffold one minimal Python service (with a small HTTP API and tests) under `services/` to make the demo runnable without Docker.
