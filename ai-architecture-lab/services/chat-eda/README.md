# Chat EDA — Event-Driven Example

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
