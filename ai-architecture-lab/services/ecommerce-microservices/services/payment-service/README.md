# Payment Service (ecommerce microservices)

Summary
-------
Placeholder README for the Payment service. The payment service handles payment authorization and settlement and exposes endpoints for charging and refunding orders.

What this demonstrates
----------------------
- Integration with payment gateways (simulated in the lab)
- Handling transient failures and retries

Tech
----
- Can be implemented with a lightweight HTTP API and a fake payment provider for local testing.

Quick start / scaffold
----------------------
Add a small FastAPI service here that exposes endpoints like `/charge` and `/refund`. For tests, provide a fake gateway implementation.

Notes for learners
------------------
- Payment systems require careful handling of retries, reconciliation, and idempotency. Keep the example focused on the basic flow for learning.
