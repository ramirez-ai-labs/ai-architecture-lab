# Data Transfer Object (DTO) Pattern Kata

Simple, immutable objects for safely transferring data across system boundaries.

---

## 🌱 What Is a Data Transfer Object?

**Data Transfer Object (DTO)** is an object that carries data between different parts of a system or across network boundaries. The key rule: **DTOs have NO BEHAVIOR—only data**.

### DTO vs Domain Model

| Aspect | Domain Model | DTO |
|--------|--------------|-----|
| **Behavior** | Rich, complex business logic | None—just data |
| **Where used** | Inside services (business logic) | At boundaries (APIs, databases) |
| **Mutability** | Often mutable | Immutable (frozen) |
| **Example** | `account.deposit(100)` | `user_dto = UserDTO(id=1, name="Alice")` |

### Why Immutable?

DTOs cross boundaries (networks, processes, threads). Making them immutable:
- Prevents accidental modification
- Makes them thread-safe
- Easier to reason about
- Predictable serialization

---

## 🎓 Why Use DTOs?

### Benefits

1. **Serializable**: Easy to convert to JSON, XML, Protocol Buffers
2. **Boundary clarity**: Explicit contract at system boundaries
3. **Language-agnostic**: Can be used in different languages
4. **Decoupled**: Changes to internal representation don't affect external APIs
5. **Fast**: No overhead of complex object behaviors

### When to Use

- ✅ API responses/requests (REST, GraphQL)
- ✅ Database queries (map rows to objects)
- ✅ Message payloads (RabbitMQ, Kafka)
- ✅ RPC/service calls

### When NOT to Use

- ❌ Inside business logic (use Domain Models)
- ❌ When you need complex behavior
- ❌ For internal-only data structures

---

## 📁 Structure

```
dto/
├── dto.py                      # DTO base class and concrete DTOs
├── examples/
│   └── api_serialization.py   # Example: JSON serialization flow
├── tests/
│   └── test_dto.py            # 24 comprehensive tests
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ai-architecture-lab/katas/base-patterns/dto
pip install -r requirements.txt
```

### 2. Run Tests

```bash
# Run all tests
pytest -v

# Run specific test class
pytest tests/test_dto.py::TestDTOSerialization -v
```

### 3. Explore the Code

Start with:
1. `dto.py` — UserDTO and ProductDTO implementations
2. `examples/api_serialization.py` — Real-world API flow
3. `tests/test_dto.py` — Comprehensive test suite

---

## 💡 Usage Examples

### Creating DTOs

```python
from dto import UserDTO, ProductDTO

# Create UserDTO
user = UserDTO(id=1, name="Alice", email="alice@example.com", is_active=True)

# Create ProductDTO (optional fields default to None)
product = ProductDTO(id=1, name="Laptop", price_cents=99900)

# Optional fields can be provided
product = ProductDTO(
    id=1,
    name="Laptop",
    price_cents=99900,
    description="High-performance laptop",
    stock_available=5
)
```

### Serialization (for APIs)

```python
# Convert DTO to dict (for JSON serialization)
user_dict = user.to_dict()
# {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'is_active': True}

# Send as JSON in API response
import json
json_response = json.dumps(user_dict)
```

### Deserialization (from APIs)

```python
# Client receives JSON
request_data = {
    "id": 1,
    "name": "Bob",
    "email": "bob@example.com",
    "is_active": True
}

# Convert to DTO
user = UserDTO.from_dict(request_data)
```

### Database Mapping

```python
# Database returns rows as dicts
db_rows = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "is_active": True},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "is_active": True},
]

# Convert to DTOs
users = [UserDTO.from_dict(row) for row in db_rows]

# Use in service
for user in users:
    print(f"{user.name}: {user.email}")
```

### Immutability

```python
user = UserDTO(id=1, name="Alice", email="alice@example.com")

# DTOs are immutable (frozen dataclasses)
user.name = "Bob"  # Raises FrozenInstanceError

# This is a feature—prevents accidental modifications
```

---

## 🧪 Test Coverage

This kata includes **24 comprehensive tests** organized into 7 test classes:

**Creation Tests (5)**
- Creating with all fields
- Creating with default values
- Required field validation

**Immutability Tests (3)**
- Cannot modify UserDTO
- Cannot modify ProductDTO
- Thread-safe immutability

**Serialization Tests (6)**
- DTO to dict conversion
- Dict to DTO creation
- Handling None values
- Ignoring extra fields
- Round-trip conversion

**Equality Tests (3)**
- Equal DTOs with same fields
- Unequal DTOs with different fields
- Value-based equality

**Representation Tests (2)**
- Readable string representations

**Boundary Usage Tests (3)**
- Database to API flow
- API request to DTO flow
- Multiple DTO formats

**Advanced Tests (2)**
- Optional field handling
- DTO composition

Run tests to see all patterns in action:

```bash
pytest tests/test_dto.py -v
```

---

## 🔗 Related Patterns

- **Service Layer** (`../../../domain-logic/service_layer/`) — Uses DTOs at boundaries
- **Data Mapper** — Converts DTOs to domain objects
- **Repository** — Returns DTOs for queries
- **Domain Model** (`../../../domain-logic/domain_model/`) — Complex logic; DTOs carry data

---

## 📚 Learning Path

1. **Start here**: Understand DTO as data-only container
2. **Try serialization**: Convert DTOs to/from JSON
3. **Explore immutability**: See why frozen dataclasses matter
4. **Build a boundary**: Map database rows → DTOs → API responses
5. **Next kata**: Move to Gateway pattern to see DTOs in action

---

## 🎯 Key Takeaways

1. **DTOs are data containers** — No behavior, no business logic
2. **Immutability prevents bugs** — Frozen dataclasses ensure predictability
3. **Serialization is easy** — Python dataclasses convert to/from dicts trivially
4. **Boundary clarity** — DTOs make system boundaries explicit
5. **Decouple layers** — Internal changes don't affect external contracts

---

## 📝 Notes

- **Immutable by default**: Use `frozen=True` on all DTOs
- **Optional fields**: Use `Optional[Type]` with `= None` default
- **No validation in DTO**: Keep validation in domain layer
- **Serialization**: `to_dict()` and `from_dict()` handle conversion
- **Use dataclasses**: Built-in Python feature, generates `__init__`, `__eq__`, etc.

---

**Next Steps:** After understanding DTOs, explore `Gateway/Adapter` to see how DTOs are used when wrapping external systems.
