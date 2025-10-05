# Ecommerce Microservices Architecture

This directory contains multiple small services (order, payment, inventory, api-gateway) that communicate via REST and optionally an event bus for asynchronous integration.

Notes:
- Use events for eventual consistency (e.g., order.created -> inventory.reserved)
- Provide clear topic names and event contracts (see root `docs/` for templates)
- Docker Compose is included for local integration testing
