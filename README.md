# ai-architecture-showcase
A hands-on collection of software architecture projects demonstrating modern design patterns from layered and microservices to event-driven, CQRS, and AI-integrated systems.

---

## AI Architecture Lab — Repo & Pattern Mapping (PoEAA)

**Purpose:** Maps PoEAA patterns to example services in the AI Architecture Lab GitHub repository, including why each pattern is used and the typical enterprise tech stack for real-world applications.

---

Below is a curated mapping of commonly used Patterns of Enterprise Application Architecture (PoEAA) to services and modules in this repository. Use this as a quick reference when exploring the lab and when deciding which example to run or extend.

---

### 1️⃣ Domain Logic Patterns

| Pattern            | Confluence Page                   | GitHub Service                   | Why / Purpose                                                                                  | Typical Tech Stack                             | Fowler Pattern Name | Notes / Insights                                          |
| ------------------ | --------------------------------- | -------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------- | ------------------- | --------------------------------------------------------- |
| Transaction Script | Domain Logic → Transaction Script | services/blog-cms/transaction_script_example | Handles simple CRUD per request; keeps logic procedural for small CMS workflows                | Python/FastAPI, Node/Express, PostgreSQL/MySQL | Transaction Script  | Simple, small-scale logic; easy to follow and debug       |
| Table Module       | Domain Logic → Table Module       | services/ecommerce-microservices | Centralizes business rules for all rows in a table; reduces duplication                        | Java/Spring Boot, PostgreSQL, Hibernate        | Table Module        | Ideal for batch processing and consistent domain logic    |
| Domain Model       | Domain Logic → Domain Model       | services/chat-eda                | Rich objects represent domain entities with behavior; needed for AI pipelines                  | Python/FastAPI, SQLAlchemy, Redis              | Domain Model        | Maintains complex domain logic; testable and maintainable |
| Service Layer      | Domain Logic → Service Layer      | services/bank-cqrs/simple_cqrs   | Defines application's boundary with a layer of services that coordinates application responses | Java/Spring Boot, REST/GraphQL                 | Service Layer       | Encapsulates domain logic and external API access         |

---

### 2️⃣ Data Source Patterns

| Pattern            | Confluence Page                  | GitHub Service    | Why / Purpose                                                             | Typical Tech Stack                      | Fowler Pattern Name | Notes / Insights                                             |
| ------------------ | -------------------------------- | ----------------- | ------------------------------------------------------------------------- | --------------------------------------- | ------------------- | ------------------------------------------------------------ |
| Table Data Gateway | Data Source → Table Data Gateway | common/db         | Encapsulates table-level CRUD; simplifies DB access                       | Java/Spring, JDBC, PostgreSQL           | Table Data Gateway  | Reusable across multiple services                            |
| Row Data Gateway   | Data Source → Row Data Gateway   | common/db         | Provides row-level operations; used in bank-cqrs for transactional safety | Java/Spring, Hibernate, Oracle DB       | Row Data Gateway    | Supports fine-grained transaction handling                   |
| Active Record      | Data Source → Active Record      | services/blog-cms | Entities persist themselves; simple approach for lightweight CMS          | Rails (ActiveRecord), SQLite/PostgreSQL | Active Record       | Mixes domain and persistence; good for small apps            |
| Data Mapper        | Data Source → Data Mapper        | services/chat-eda | Separates domain logic from DB; critical for AI pipelines                 | Python/SQLAlchemy, PostgreSQL, Redis    | Data Mapper         | Supports complex transformations and testable domain objects |

---

### 3️⃣ Object-Relational Behavioral Patterns

| Pattern                       | Confluence Page   | GitHub Service                   | Why / Purpose                                                        | Typical Tech Stack             | Fowler Pattern Name           | Notes / Insights                                   |
| ----------------------------- | ----------------- | -------------------------------- | -------------------------------------------------------------------- | ------------------------------ | ----------------------------- | -------------------------------------------------- |
| Identity Map                  | OR → Identity Map | services/bank-cqrs/simple_cqrs   | Ensures a single instance per entity is loaded; prevents duplication | Java/Hibernate, Redis          | Identity Map                  | Improves consistency; reduces memory load          |
| Unit of Work                  | OR → Unit of Work | services/chat-eda                | Tracks object changes; commits once for efficiency                   | Python/SQLAlchemy, PostgreSQL  | Unit of Work                  | Useful for batch operations or AI model updates    |
| Lazy Load                     | OR → Lazy Load    | services/ecommerce-microservices | Defers expensive DB loads until needed; improves performance         | Java/Hibernate, MySQL          | Lazy Load                     | Reduces unnecessary queries                        |
| Optimistic / Pessimistic Lock | OR → Locking      | services/bank-cqrs/simple_cqrs   | Ensures safe concurrent updates                                      | Java/Spring, PostgreSQL/Oracle | Optimistic / Pessimistic Lock | Needed for high-concurrency financial transactions |

---

### 4️⃣ Web Presentation Patterns

| Pattern          | Confluence Page                     | GitHub Service                   | Why / Purpose                                                    | Typical Tech Stack                         | Fowler Pattern Name   | Notes / Insights                                |
| ---------------- | ----------------------------------- | -------------------------------- | ---------------------------------------------------------------- | ------------------------------------------ | --------------------- | ----------------------------------------------- |
| MVC              | Web Presentation → MVC              | services/blog-cms                | Separates UI, controller, and domain logic                       | Python/Django, Node/Express, React/Angular | Model View Controller | Standard architecture for maintainable web apps |
| Page Controller  | Web Presentation → Page Controller  | services/blog-cms                | Handles requests per page                                        | Node/Express, Spring MVC                   | Page Controller       | Simple route-specific logic                     |
| Front Controller | Web Presentation → Front Controller | services/ecommerce-microservices | Central entry point for all requests; scalable for microservices | Java/Spring Boot, Nginx                    | Front Controller      | Makes routing uniform and maintainable          |

---

### 5️⃣ Concurrency & Integration Patterns

| Pattern                 | Confluence Page             | GitHub Service                   | Why / Purpose                                                 | Typical Tech Stack                            | Fowler Pattern Name     | Notes / Insights                                         |
| ----------------------- | --------------------------- | -------------------------------- | ------------------------------------------------------------- | --------------------------------------------- | ----------------------- | -------------------------------------------------------- |
| Thread Pool             | Concurrency → Thread Pool   | services/chat-eda                | Limits concurrent AI inferences; prevents resource exhaustion | Python/ThreadPoolExecutor, Celery, Kubernetes | Thread Pool             | Efficient handling of multiple requests                  |
| Active Object           | Concurrency → Active Object | services/chat-eda                | Decouples method invocation from execution; async processing  | Python/AsyncIO, FastAPI, RabbitMQ             | Active Object           | Enables responsive pipelines                             |
| Scheduler / Timer       | Concurrency → Scheduler     | scripts/cron-jobs                | Handles recurring tasks for services                          | Linux Cron, Airflow, Celery Beat              | Scheduler / Timer       | Useful for maintenance and batch jobs                    |
| Remote Facade           | Integration → Remote Facade | services/ecommerce-microservices | Simplifies service-to-service interactions                    | Java/Spring Boot, REST/GraphQL, Nginx         | Remote Facade           | Reduces network complexity                               |
| Gateway / Adapter       | Integration → Gateway       | common/adapters                  | Bridges incompatible service APIs                             | Python/FastAPI, Node/Express, Kafka           | Gateway / Adapter       | Standardizes communication between heterogeneous systems |
| Message Bus / Messaging | Integration → Messaging     | services/ecommerce-microservices | Implements event-driven communication                         | RabbitMQ, Kafka, Redis Streams                | Message Bus / Messaging | Supports decoupled, scalable systems                     |
| Service Layer           | Integration → Service Layer | services/bank-cqrs/simple_cqrs   | Provides a uniform API for business operations                | Java/Spring Boot, REST/GraphQL                | Service Layer           | Encapsulates domain logic for external clients           |

---

### 6️⃣ Distribution Patterns

| Pattern              | Confluence Page              | GitHub Service                   | Why / Purpose                                | Typical Tech Stack                    | Fowler Pattern Name  | Notes / Insights                              |
| -------------------- | ---------------------------- | -------------------------------- | -------------------------------------------- | ------------------------------------- | -------------------- | --------------------------------------------- |
| Remote Facade        | Distribution → Remote Facade | services/ecommerce-microservices | Coarse-grained facade to reduce remote calls | Java/Spring Boot, REST/GraphQL, Nginx | Remote Facade        | Optimizes performance over network            |
| Data Transfer Object | Distribution → DTO           | common/dto                       | Transfers data between layers/services       | Java, Python, JSON, Protobuf          | Data Transfer Object | Reduces network chatter; serializable objects |

---

### 7️⃣ Offline Concurrency Patterns

| Pattern                  | Confluence Page                      | GitHub Service     | Why / Purpose                                     | Typical Tech Stack             | Fowler Pattern Name      | Notes / Insights                         |
| ------------------------ | ------------------------------------ | ------------------ | ------------------------------------------------- | ------------------------------ | ------------------------ | ---------------------------------------- |
| Optimistic Offline Lock  | Offline Concurrency → Optimistic     | services/bank-cqrs/simple_cqrs | Detects conflicts and rolls back transactions     | Java/Spring, PostgreSQL/Oracle | Optimistic Offline Lock  | Useful for low-contention scenarios      |
| Pessimistic Offline Lock | Offline Concurrency → Pessimistic    | services/bank-cqrs/simple_cqrs | Allows only one transaction at a time             | Java/Spring, PostgreSQL/Oracle | Pessimistic Offline Lock | Needed for high-contention scenarios     |
| Coarse-Grained Lock      | Offline Concurrency → Coarse-Grained | services/bank-cqrs/simple_cqrs | Locks a set of related objects with a single lock | Java/Spring, PostgreSQL/Oracle | Coarse-Grained Lock      | Simplifies complex transactional control |
| Implicit Lock            | Offline Concurrency → Implicit       | services/bank-cqrs/simple_cqrs | Allows framework code to acquire offline locks    | Java/Spring, PostgreSQL/Oracle | Implicit Lock            | Used by frameworks to manage concurrency |

---

### 8️⃣ Session State Patterns

| Pattern                | Confluence Page                  | GitHub Service    | Why / Purpose                 | Typical Tech Stack             | Fowler Pattern Name    | Notes / Insights                              |
| ---------------------- | -------------------------------- | ----------------- | ----------------------------- | ------------------------------ | ---------------------- | --------------------------------------------- |
| Client Session State   | Session → Client Session State   | services/blog-cms | Stores session data on client | Cookies, JWT, LocalStorage     | Client Session State   | Offloads server; good for small session data  |
| Server Session State   | Session → Server Session State   | services/blog-cms | Stores session data on server | Redis, Memcached, Node/Express | Server Session State   | Centralized control; supports larger sessions |
| Database Session State | Session → Database Session State | common/db         | Stores session data in DB     | PostgreSQL, MySQL, SQLAlchemy  | Database Session State | Persistent; suitable for enterprise workloads |

---

### 9️⃣ Base Patterns

| Pattern             | Confluence Page            | GitHub Service    | Why / Purpose                                              | Typical Tech Stack            | Fowler Pattern Name | Notes / Insights                      |
| ------------------- | -------------------------- | ----------------- | ---------------------------------------------------------- | ----------------------------- | ------------------- | ------------------------------------- |
| Gateway             | Base → Gateway             | common/adapters   | Encapsulates access to external systems                    | Python/FastAPI, Java/Spring   | Gateway             | Abstracts external system interaction |
| Service Stub        | Base → Service Stub        | tests/stubs       | Removes dependency on problematic services during testing  | WSDL, MockServer, Python/Node | Service Stub        | Enables isolated testing              |
| Record Set          | Base → Record Set          | common/db         | In-memory tabular representation                           | Java, Python                  | Record Set          | Lightweight DB-like object            |
| Mapper              | Base → Mapper              | common/mappers    | Maps between independent objects                           | Python/Java                   | Mapper              | Useful for decoupled systems          |
| Layer Supertype     | Base → Layer Supertype     | common/core       | Supertype for all types in a layer                         | Java, Python                  | Layer Supertype     | Standardizes common behavior          |
| Separated Interface | Base → Separated Interface | common/interfaces | Interface defined separately from implementation           | Java, Python                  | Separated Interface | Improves modularity                   |
| Registry            | Base → Registry            | common/registry   | Well-known object for locating shared services             | Java, Python                  | Registry            | Centralizes service lookup            |
| Value Object        | Base → Value Object        | common/models     | Immutable small object, equality by value                  | Java, Python                  | Value Object        | Examples: money, date range           |
| Money               | Base → Money               | common/models     | Represents monetary value                                  | Java, Python                  | Money               | Specialization of Value Object        |
| Special Case        | Base → Special Case        | common/models     | Subclass providing special behavior                        | Java, Python                  | Special Case        | Handles edge cases                    |
| Plugin              | Base → Plugin              | common/plugins    | Links classes during configuration rather than compilation | Java, Python                  | Plugin              | Useful for pluggable architectures    |

---

If you'd like, I can also add quick badges and a short table of 'how to run' example services (FastAPI/Node/Java) so new contributors can boot an example locally.
