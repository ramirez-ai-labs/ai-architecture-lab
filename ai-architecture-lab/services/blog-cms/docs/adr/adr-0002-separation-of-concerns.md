# ADR 0002 - Separation of Concerns: Layered Architecture

Date: 2025-10-05
Status: Accepted

Context

We want the Blog CMS to be modular, testable, and easy to evolve. The system will be worked on by multiple contributors and should have clear boundaries between transport, orchestration, domain logic, and persistence.

Decision

Adopt a layered architecture with the following layers:

- Presentation: HTTP/GraphQL controllers and routes
- Application: Use cases / application services that orchestrate domain operations
- Domain: Entities, value objects, domain services, and repository interfaces
- Infrastructure: Implementations for repositories, external integrations, notification adapters, and plugins

Consequences

- Pros: Improved testability, clearer responsibilities, easier to reason about domain logic and to swap infrastructure implementations.
- Cons: More boilerplate and need for discipline to keep boundaries clean.

Notes

- Keep repository interfaces in `domain/repositories` and implementations in `infrastructure/persistence`.
- Emit domain events from the domain layer; publishing should be handled by the infrastructure layer.
