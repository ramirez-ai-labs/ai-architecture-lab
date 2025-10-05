# ADR 0001 - Ecommerce Initial Decision

Decision: Model the ecommerce system as small, focused microservices with an API gateway for routing. Use a message bus for cross-service events.

Consequences:
- Easier independent deployment and scaling
- Need for operational maturity (observability, tracing, retries)
