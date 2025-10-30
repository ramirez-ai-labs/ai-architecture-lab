# Inventory Service (ecommerce microservices)

Summary
-------
Placeholder README for the Inventory service. The inventory service is responsible for tracking stock levels and exposing APIs to decrement/increment stock when orders are placed or cancelled.

What this demonstrates
----------------------
- Table Data Gateway / Repository for handling product inventory
- Integration with orders via synchronous or asynchronous messaging

Tech
----
- Any language or framework for an HTTP API; backed by a simple SQL store or in-memory store for experiments.

Quick start / scaffold
----------------------
Create a small HTTP service here (FastAPI) that exposes endpoints like `/products` and `/products/{id}/reserve`.

Notes for learners
------------------
- Keep inventory operations idempotent and consider concurrency controls (optimistic/pessimistic locks) when simulating real systems.
