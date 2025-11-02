# Chat EDA — Event-Driven & Domain Examples

Summary
-------
Small examples demonstrating event-driven architecture for a chat application and a Domain Model example that encapsulates behavior in rich entities.

What this demonstrates
----------------------
- Event-driven architecture for decoupled components (see `broker/` placeholders)
- Domain Model: `domain_model_example/` shows rich entities (`Conversation`, `Message`) and a Data Mapper / Repository
- How to structure services and broker configs in a small lab

Tech
----
- Python (service examples), message broker concepts (Kafka/RabbitMQ), SQLite for simple persistence

Pattern examples
----------------
- `domain_model_example/` — Domain Model: rich entities with behavior plus a simple Data Mapper / Repository. See `domain_model_example/README.md`.
- (Planned) `orm_patterns/` — Object-relational behavioral patterns such as Unit of Work and Identity Map (not implemented yet).

Quick notes
-----------
- The `broker/` folder contains examples and placeholders for broker setup and local testing.
- Implementation code for experiments can be added under `src/` or as self-contained example folders that include README and tests.

Running / testing
-----------------
To run the domain model example tests from the repo root:

```powershell
cd ai-architecture-lab/services/chat-eda/domain_model_example
pytest -q
```

If you'd like, I can scaffold a minimal publisher and consumer (with tests) to make the event-driven example runnable and integrated with the domain model.
# Chat EDA — Event-Driven Example

<<<<<<< HEAD
Summary
-------
Small example demonstrating an event-driven architecture for a chat application. The repo contains a `broker/` folder with placeholder configs and notes about how messages flow between components.

What this demonstrates
----------------------
- Event-driven architecture for decoupled components
- Message publishing and subscription patterns
- How to structure services and broker configs in a small lab

Tech
----
- Python (service examples), message broker concepts (Kafka/RabbitMQ)

Quick notes
-----------
- The `broker/` folder contains examples and placeholders for broker setup and local testing.
- Implementation code is under `src/` for experiments and can be expanded into services that publish/consume chat events.

Running / testing
-----------------
This example is primarily illustrative. To run a local broker + services you can wire up the `broker/` configs to a local Kafka or RabbitMQ instance and add small publishers/consumers under `src/`.

If you'd like, I can scaffold a minimal publisher and consumer (with tests) to make this example runnable.
=======
Event-driven chat application examples and educational code showing Domain Model and event-driven patterns.

Overview
--------
This service hosts examples that illustrate event-driven architecture and domain modeling for a chat application.

Pattern examples
----------------
- `domain_model_example/` — Domain Model: rich entities (`Conversation`, `Message`) with behavior, plus a simple Data Mapper / Repository. Run `ai-architecture-lab/services/chat-eda/domain_model_example/README.md` for instructions.
- (Planned) `orm_patterns/` — Object-relational behavioral patterns such as Unit of Work and Identity Map (not implemented yet).

Docs
----
- `docs/architecture.md` — architecture overview for chat-eda

How to run examples
-------------------
From the repo root run the example tests:

```powershell
cd ai-architecture-lab/services/chat-eda/domain_model_example
pytest -q
```

If you'd like the example expanded into a small API or integrated with the `broker/` to show domain events, I can scaffold that next.
# Chat EDA

Event-driven chat application example. Includes broker/ for message broker configs.
>>>>>>> c2adc14 (docs(services): normalize service READMEs and add blog-cms README)
