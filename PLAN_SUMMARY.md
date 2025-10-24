# PoEAA Pattern → Repository Mapping Table

This table maps each **Enterprise Application Architecture (PoEAA)** pattern to its location in your repository, where it appears in your roadmap, and how it should be demonstrated.

Format:  
**Pattern — Repo/service — Roadmap mapping — How to demonstrate**

---

## 1️⃣ Domain Logic Patterns

**Transaction Script** — `services/blog-cms`  
Roadmap: already done (Transaction Script example).  
Demonstrate: procedural handlers that open DB, run SQL, commit, return DTOs (`transaction_script_example`).

**Table Module** — `services/ecommerce-microservices`  
Roadmap: Todo 5 “Table Module (ecommerce)” → implement `services/ecommerce-microservices/table_module_example`.  
Demonstrate: centralized table-level functions for batch operations (batch pricing update, nightly processing).

**Domain Model** — `services/chat-eda`  
Roadmap: Todo 2 “Domain Model (chat-eda)” → implement `services/chat-eda/domain_model_example`.  
Demonstrate: rich entities with behavior, unit tests of domain methods, persistence via Data Mapper/Repository.

**Service Layer** — `services/bank-cqrs`  
Roadmap: Todo 4 “Service Layer (bank-cqrs)” → implement `services/bank-cqrs/service_layer_example`.  
Demonstrate: application boundary services that orchestrate domain objects, enforce transactions and validation.

---

## 2️⃣ Data Source Patterns

**Table Data Gateway** — `common/db`  
Roadmap: Todo 13/14 “Base patterns / common/” → implement under `common/db`.  
Demonstrate: gateway module encapsulating CRUD per table, used by examples.

**Row Data Gateway** — `common/db`  
Roadmap: same as Table Data Gateway → `common/db/row_data_gateway_example`.  
Demonstrate: row-level object with CRUD methods; show transactional usage in bank-cqrs.

**Active Record** — `services/blog-cms`  
Roadmap: Todo 3 “Active Record (blog-cms)” → `services/blog-cms/active_record_example`.  
Demonstrate: model objects with `.save()` / `.update()` semantics (Peewee or Rails).

**Data Mapper** — `services/chat-eda`  
Roadmap: covered by Todo 2 & 6 — Domain Model + ORM patterns.  
Demonstrate: repository/data-mapper mapping domain objects ↔ SQLAlchemy rows.

---

## 3️⃣ Object-Relational Behavioral Patterns

**Identity Map** — `services/bank-cqrs`  
Roadmap: Todo 6 “ORM patterns (Unit of Work / Identity Map)” → `services/chat-eda/orm_patterns`.  
Demonstrate: ensure single instance per ID when loading multiples; show caching inside a Unit of Work.

**Unit of Work** — `services/chat-eda`  
Roadmap: Todo 6 — implement Unit of Work after Domain Model.  
Demonstrate: collect changes to entities and commit once.

**Lazy Load** — `services/ecommerce-microservices`  
Roadmap: Todo 5/6 — show lazy loading via SQLAlchemy deferred loads or ORM proxies.  
Demonstrate: lazy association loading.

**Optimistic / Pessimistic Lock** — `services/bank-cqrs`  
Roadmap: Todo 4/6 — demonstrate concurrency controls (DB version column for optimistic; `SELECT FOR UPDATE` for pessimistic).

---

## 4️⃣ Web Presentation Patterns

**MVC** — `services/blog-cms`  
Roadmap: Todo 7 “MVC example” → `services/blog-cms/mvc_example`.  
Demonstrate: models, views, templates; clear separation of concerns.

**Page Controller** — `services/blog-cms`  
Roadmap: Todo 8 “Page Controller example” → `services/blog-cms/page_controller_example`.  
Demonstrate: per-page handlers that render templates and perform logic.

**Front Controller** — `services/ecommerce-microservices`  
Roadmap: Todo 11/13 — part of ecommerce gateway examples.  
Demonstrate: single entry point that routes requests to internal services (e.g., Nginx or app router).

---

## 5️⃣ Concurrency & Integration Patterns

**Thread Pool** — `services/chat-eda`  
Roadmap: Todo 11 “Concurrency & Integration examples” → `services/chat-eda/thread_pool_example`.  
Demonstrate: limit inference concurrency with ThreadPoolExecutor or worker pool.

**Active Object** — `services/chat-eda`  
Roadmap: Todo 11 → `services/chat-eda/active_object_example`.  
Demonstrate: decouple call and execution using queues/actors (asyncio or message queue).

**Scheduler / Timer** — `scripts/cron-jobs`  
Roadmap: Todo 11 or separate scripts folder.  
Demonstrate: recurring batch jobs (Airflow/Celery Beat).

**Remote Facade** — `services/ecommerce-microservices`  
Roadmap: Todo 5/12 — implement API facade.  
Demonstrate: facade service aggregating multiple microservices into a single coarse-grained endpoint.

**Gateway / Adapter** — `common/adapters`  
Roadmap: Todo 13 — implement `common/adapters/gateway_example`.  
Demonstrate: adapter wrapping external API (e.g., payment gateway).

**Message Bus / Messaging** — `services/ecommerce-microservices`  
Roadmap: Todo 11 — `message_bus_example` using RabbitMQ/Kafka.  
Demonstrate: async message handling between services.

**Service Layer (integration)** — `services/bank-cqrs`  
Roadmap: Todo 4 — show service layer for external client interfaces.

---

## 6️⃣ Distribution Patterns

**Remote Facade** — `services/ecommerce-microservices`  
Roadmap: Todo 5/12 — implement as API façade.  
Demonstrate: coarse-grained API layer.

**Data Transfer Object (DTO)** — `common/dto`  
Roadmap: Todo 12 — add `common/dto` and demonstrate DTO usage across services and Remote Facade.

---

## 7️⃣ Offline Concurrency Patterns

**Optimistic Offline Lock** — `services/bank-cqrs`  
Roadmap: Todo 4/6 — show versioned rows and conflict detection.

**Pessimistic Offline Lock** — `services/bank-cqrs`  
Roadmap: same as above — demonstrate `SELECT FOR UPDATE` or DB locks.

**Coarse-Grained Lock** — `services/bank-cqrs`  
Roadmap: same — demonstrate locking of related aggregates.

**Implicit Lock** — `services/bank-cqrs`  
Roadmap: show how frameworks (ORM/DB) manage implicit locking automatically.

---

## 8️⃣ Session State Patterns

**Client Session State** — `services/blog-cms`  
Roadmap: Todo 9/13 — `client_session_example`.  
Demonstrate: JWT issuance, localStorage usage, token renewal.

**Server Session State** — `services/blog-cms`  
Roadmap: Todo 10/14 — `server_session_example`.  
Demonstrate: server-side sessions using Redis or FastAPI middleware.

**Database Session State** — `common/db` or `common/session`  
Roadmap: Todo 13 — DB-backed sessions example.

---

## 9️⃣ Base Patterns

**Gateway** — `common/adapters`  
Roadmap: Todo 13 — `gateway_example`.  
Demonstrate: wrapper around external service.

**Service Stub** — `tests/stubs`  
Roadmap: Todo 13 — mock external services in tests.

**Record Set** — `common/db`  
Roadmap: Todo 13 — in-memory table representation.

**Mapper** — `common/mappers`  
Roadmap: Todo 13 — DTO ↔ domain mapping utilities.

**Layer Supertype** — `common/core`  
Roadmap: Todo 13 — base classes and examples for layers.

**Separated Interface** — `common/interfaces`  
Roadmap: Todo 13 — interface examples and adapters.

**Registry** — `common/registry`  
Roadmap: Todo 13 — service locator for tests.

**Value Object** — `common/models`  
Roadmap: Todo 13 — implement `ValueObject` examples (`Money`, `DateRange`).

**Money** — `common/models`  
Roadmap: Todo 13 — `Money` value object with tests.

**Special Case** — `common/models`  
Roadmap: Todo 13 — `SpecialCase` subclass example.

**Plugin** — `common/plugins`  
Roadmap: Todo 13 — plugin loading
