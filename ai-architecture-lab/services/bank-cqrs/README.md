# Bank CQRS

Example demonstrating CQRS and Event Sourcing with separate command and query services and an event store.

Overview
--------
This service contains an example implementation that demonstrates the CQRS (Command Query Responsibility Segregation)
pattern and Event Sourcing. See `docs/` for architecture details and ADRs.

Pattern examples
----------------
- (Planned) `service_layer_example/` — Service Layer orchestration and transaction boundaries (not implemented yet).

Docs
----
- `docs/architecture.md` — service architecture overview
- `docs/adr/adr-0001-design-decision.md` — initial design ADR

How to run examples
-------------------
Each example under this service (when present) includes a README with run/test instructions. General pattern:

```powershell
cd ai-architecture-lab/services/bank-cqrs/<example_folder>
pytest -q
```

If you'd like, I can scaffold the `service_layer_example` here and add tests and a README.
# Bank CQRS

Example demonstrating CQRS and Event Sourcing with separate command and query services and an event store.
# Bank CQRS

CQRS + Event Sourcing example. See `docs/` for architecture details.

Docs:
- `docs/architecture.md` - service architecture overview
- `docs/adr/adr-0001-design-decision.md` - initial design ADR
