# Blog CMS

A sample Blog Content Management System (CMS) built using a **layered architecture**.  
The project includes a structured `src/` directory for source code and a `tests/` directory for unit and integration tests.

---

## 🧱 Architecture (Layered)

```mermaid
flowchart TD
  title[Layered Blog/CMS Architecture]

  subgraph Presentation
    A[HTTP / GraphQL Controllers]
  end

  subgraph Application
    B[Use Cases / Application Services]
  end

  subgraph Domain
    C[Entities & Domain Services]
    D[Repository Interfaces]
  end

  subgraph Infrastructure
    E[Database / External APIs / Framework Integrations]
  end

  A --> B --> C --> D --> E
