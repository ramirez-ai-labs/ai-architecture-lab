# Blog CMS

Layered architecture example service. Contains src/ and tests/ directories.

## Architecture (Layered)

```mermaid
flowchart TD
  title Layered Blog/CMS Architecture

  subgraph Presentation
    A[HTTP / GraphQL Controllers]
  end

  subgraph Application
    B[Use Cases / Application Services]
  end

  subgraph Domain
    C[Entities & Domain Services]
    D[Repository Interfaces]
  ```

See `docs/architecture.md` for more details.