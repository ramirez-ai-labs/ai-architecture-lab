# Blog CMS

A sample **Blog Content Management System (CMS)** built using a **layered architecture**.  
This project serves as a **software architecture showcase**, demonstrating clear separation of concerns, the repository pattern, and simple event-driven hooks.

---

## 📁 Directory Highlights
- `src/` — application source (presentation, application, domain, infrastructure)
- `tests/` — unit and integration tests
- `docs/` — architecture docs, ADRs, and diagrams

---

## 🧱 Architecture (Layered)

```mermaid
flowchart TD

  %% Title
  %% (GitHub Mermaid doesn't support top-level titles, so we comment it)
  %% Layered Blog/CMS Architecture

  subgraph Presentation
    A["HTTP or GraphQL Controllers"]
  end

  subgraph Application
    B["Use Cases / Application Services"]
  end

  subgraph Domain
    C["Entities & Domain Services"]
    D["Repository Interfaces"]
    E["Domain Events"]
  end

  subgraph Infrastructure
    F["Repository Implementations (DB)"]
    G["Notification / Event Bus"]
    H["Plugin Adapters"]
  end

  A --> B
  B --> C
  B --> D
  D --> F
  C --> E
  E --> G
  H --> B
