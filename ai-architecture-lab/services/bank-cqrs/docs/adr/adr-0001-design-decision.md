# ADR 0001 - Bank CQRS Initial Design

Decision: Use CQRS with Event Sourcing for the banking domain to provide clear separation of command and query concerns and an auditable event log.

Consequences:
- Strong auditability and replayability
- Increased complexity in maintaining read models and eventual consistency
