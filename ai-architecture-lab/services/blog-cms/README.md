# Blog CMS

Layered architecture example service. Contains src/ and tests/ directories.

## Architecture (Layered)

```mermaid
flowchart TD
  subgraph Presentation
    A[HTTP / GraphQL Controllers]
  end

  subgraph Application
    B[Use Cases / Application Services]
  end

  subgraph Domain
    C[Entities & Domain Services]
    D[Repository Interfaces]
    E[Domain Events]
  end

  subgraph Infrastructure
    F[Repository Implementations - DB]
    G[Notification / Event Bus]
    H[Plugin Adapters]
  end

  A --> B --> C
  B --> D
  D --> F
  C --> E --> G
  H --> B
```
  A --> B --> C
  B --> D
  D --> F
  C --> E --> G
  H --> B
```

See `docs/architecture.md` for more details.