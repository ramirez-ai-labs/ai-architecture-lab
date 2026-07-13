# Service Layer Kata

## Overview

This kata teaches you the **Service Layer pattern** - how to build a layer that coordinates business logic, enforces rules, and publishes events without coupling to databases or frameworks.

## Learning Objectives

- ✅ Understand the Service Layer pattern and its role in clean architecture
- ✅ Learn how to coordinate multiple operations atomically
- ✅ Enforce business rules at the service level
- ✅ Use dependency injection for repositories
- ✅ Publish events for decoupled subscribers
- ✅ Write tests using mocked repositories (no database needed)

## Concepts

### Account
A simple domain entity:
- `id` - unique identifier
- `owner` - account owner's name
- `balance` - current balance

### AccountService
The service layer that coordinates operations:
- **create_account()** - initializes a new account
- **deposit()** - adds money to an account
- **withdraw()** - removes money with validation
- **transfer()** - moves money between accounts atomically
- **get_balance()** - queries current balance

### Business Rules Enforced
- Deposits and withdrawals must be positive
- Withdrawals cannot exceed balance (InsufficientFunds)
- Transfers check both source and destination
- All operations publish events

### Event Publishing
Events are published for each operation to enable:
- Decoupled subscribers (read models, notifications, auditing)
- Eventual consistency patterns
- Event sourcing integration

## File Structure

```
service_layer/
├── __init__.py              # Package initialization
├── service.py               # AccountService and Account model
├── README.md                # This file
├── requirements.txt         # Dependencies
├── examples/
│   ├── __init__.py
│   └── account_operations.py
└── tests/
    ├── __init__.py
    └── test_service.py
```

## Getting Started

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Examples
```bash
python examples/account_operations.py
```

### Run Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=service --cov-report=html
```

## Key Takeaways

1. **Service Layer coordinates operations** - not a transaction script
2. **Business rules are enforced** - at the service layer boundary
3. **Dependency injection enables testing** - no database required
4. **Events decouple systems** - subscribers react to changes
5. **Atomic operations** - transfers coordinate multiple changes
6. **No framework dependencies** - pure business logic

## Architecture Pattern

```
┌──────────────────┐
│   HTTP/CLI       │  ← Input (web handler, CLI command)
│   Handler        │
└────────┬─────────┘
         │
┌────────▼──────────┐
│  Service Layer    │  ← Business rule enforcement
│  (this kata!)     │  ← Event publishing
│                   │
└────────┬──────────┘
         │
    ┌────┴────┬───────────────┐
    │          │               │
    ▼          ▼               ▼
┌────────┐ ┌────────┐  ┌────────────┐
│Repo    │ │Event   │  │Domain      │
│        │ │Pub     │  │Logic       │
└────────┘ └────────┘  └────────────┘
```

## Typical Usage

```python
# Setup
repo = InMemoryRepository()
service = AccountService(repo)

# Create accounts
alice_id = service.create_account("Alice", 1000.0)
bob_id = service.create_account("Bob", 500.0)

# Business operations
service.deposit(alice_id, 200.0)
service.withdraw(alice_id, 50.0)
service.transfer(alice_id, bob_id, 100.0)

# Query
balance = service.get_balance(alice_id)
```

## Related Katas

- **Domain Model** - How to structure rich domain objects
- **Repository** - How to abstract persistence
- **Event Sourcing** - How to build systems around events
- **CQRS** - Separating reads from writes
