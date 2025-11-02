# Ecommerce Microservices — Examples & Quick Start

Summary
-------
Collection of small microservices that form a simple e-commerce example. This folder includes a `docker-compose.yml` to run the services locally for demonstration and integration testing.

What this demonstrates
----------------------
- Microservice decomposition (API gateway, inventory, orders, payments)
- Local integration via Docker Compose
- Patterns like Remote Facade, Gateway, and message-based communication

Pattern examples
----------------
- (Planned) `table_module_example/` — Table Module pattern demonstrating centralized table logic for batch operations across services.
- `services/` — placeholders for `api-gateway`, `inventory-service`, `order-service`, `payment-service` (implement individual demos in these folders).

Tech
----
- Docker Compose, Python/HTTP services, and optional message broker for async flows

Quick start
-----------
From the `ecommerce-microservices` folder you can bring up the example with:

```powershell
cd ai-architecture-lab/services/ecommerce-microservices
docker compose up --build
```

Notes for learners
------------------
- The `services/` subfolder contains individual microservice placeholders; each can be expanded into a runnable example with its own README and tests.
- See `docs/architecture.md` for design notes and patterns used in this example.

If you want, I can scaffold one minimal Python service (with a small HTTP API and tests) under `services/` to make the demo runnable without Docker.
# Ecommerce Microservices — Collection

<<<<<<< HEAD
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
=======
Collection of small microservices that together form an e-commerce system. Used to demonstrate distribution and table-level patterns.

Overview
--------
This folder contains multiple small services (api-gateway, inventory-service, order-service, payment-service) and a `docker-compose.yml` to run them locally.

Pattern examples
----------------
- (Planned) `table_module_example/` — Table Module pattern demonstrating centralized table logic for batch operations across services.
- Services under `services/` each represent a focused microservice (see subfolders).

Docs
----
- `docs/architecture.md` — architecture overview for ecommerce microservices
- `docs/adr/` — architectural decisions

How to run examples
-------------------
Use the included compose file to run multiple services locally:

```powershell
cd ai-architecture-lab/services/ecommerce-microservices
docker-compose up --build
```

Example tests and local demos (if added) will include README files with pytest instructions.
# Ecommerce Microservices

Collection of small microservices forming an e-commerce system. Includes example docker-compose to run locally.
>>>>>>> c2adc14 (docs(services): normalize service READMEs and add blog-cms README)
