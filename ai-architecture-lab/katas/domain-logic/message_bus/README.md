# Message Bus Pattern Kata

A simple in-process event bus for decoupled, event-driven communication between domain objects and their handlers.

---

## 🌱 What Is Message Bus?

**Message Bus** (also called Event Bus or Event Dispatcher) is a pattern for coordinating behavior when something important happens in your domain without tightly coupling the cause to its effects.

Instead of domain logic directly calling handlers:

```python
# ❌ Tightly coupled
order.create()
order.send_confirmation_email()
order.update_inventory()
order.post_to_analytics()
```

You publish an event and let independent subscribers react:

```python
# ✅ Decoupled with Message Bus
order.create()
bus.publish({'type': 'order_created', 'order_id': order.id})
# Subscribers (email, inventory, analytics) react independently
```

### Key Characteristics

- ✅ **Decoupled**: Domain logic doesn't know or care who listens
- ✅ **Event-driven**: Reactions happen when events are published
- ✅ **Synchronous (for now)**: Handlers run in-process, blocking
- ✅ **Simple subscription model**: `subscribe(handler)` and `publish(event)`
- ✅ **No event storage**: Events are processed immediately (toy implementation)

---

## 🎓 Why Use Message Bus?

### Benefits

1. **Separation of concerns**: Domain logic stays clean; side effects are handled elsewhere
2. **Easy to test**: Publish events, verify handlers were called, no external dependencies
3. **Extensible**: Add new handlers without touching domain logic
4. **Clear contracts**: Events are the interface between domain and handlers
5. **Natural progression to async**: Move from sync bus → message broker (Kafka, RabbitMQ) without changing event structure

### When to Use

- ✅ Coordinating multiple side effects from a single domain action
- ✅ Decoupling domain logic from infrastructure (emails, notifications, logging)
- ✅ Building eventual-consistency workflows
- ✅ Single-process applications where async isn't critical
- ✅ Learning event-driven architecture before jumping to a message broker

### When NOT to Use

- ❌ **For critical workflows requiring durability**: Use a message broker (this bus loses events on restart)
- ❌ **For cross-service communication**: Use a durable broker (Kafka, RabbitMQ, AWS SNS/SQS)
- ❌ **When you need guaranteed ordering across services**: Use a broker with ordering guarantees
- ❌ **When handler failures must trigger retries**: This bus doesn't retry or dead-letter failed events

---

## 📁 Structure

```
message_bus/
├── message_bus.py              # Message Bus implementation
├── examples/
│   └── bank_projections.py     # Example: account events and read-model projections
├── tests/
│   └── test_message_bus.py     # 19 comprehensive tests
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ai-architecture-lab/katas/domain-logic/message_bus
pip install -r requirements.txt
```

### 2. Run Tests

```bash
# Run all tests
pytest -v

# Run specific test class
pytest tests/test_message_bus.py::TestSubscription -v
```

### 3. Explore the Code

Start with:
1. `message_bus.py` — The bus implementation (subscribe/publish functions)
2. `examples/bank_projections.py` — Real-world account event scenario
3. `tests/test_message_bus.py` — Comprehensive test suite

---

## 💡 Usage Examples

### Basic Subscription and Publishing

```python
from message_bus import subscribe, publish

# Define a handler
def on_user_created(event):
    user_id = event['user_id']
    print(f"Sending welcome email to user {user_id}")

# Subscribe the handler
subscribe(on_user_created)

# Publish an event
publish({
    'type': 'user_created',
    'user_id': 123,
    'email': 'alice@example.com',
})
# Output: Sending welcome email to user 123
```

### Multiple Independent Handlers

```python
# Multiple handlers can listen to the same event
def update_read_model(event):
    print(f"Updating read model for {event['type']}")

def send_analytics(event):
    print(f"Logging analytics for {event['type']}")

subscribe(update_read_model)
subscribe(send_analytics)

publish({'type': 'order_placed', 'order_id': 456})
# Output:
# Updating read model for order_placed
# Logging analytics for order_placed
```

### CQRS Pattern: Projections Listening to Events

```python
# A read-model projection that updates when events occur
class AccountReadModel:
    def __init__(self):
        self.accounts = {}

    def on_account_created(self, event):
        self.accounts[event['account_id']] = {
            'balance': event['initial_balance'],
            'created': True,
        }

    def on_deposit(self, event):
        acc_id = event['account_id']
        self.accounts[acc_id]['balance'] += event['amount']

# Create projection and subscribe to events
read_model = AccountReadModel()
subscribe(read_model.on_account_created)
subscribe(read_model.on_deposit)

# Domain publishes events
publish({
    'type': 'account_created',
    'account_id': 'ACC001',
    'initial_balance': 1000,
})
publish({
    'type': 'deposit_made',
    'account_id': 'ACC001',
    'amount': 500,
})

# Read model is updated
print(read_model.accounts['ACC001']['balance'])  # 1500
```

### Event Payload Structure

```python
# Events are plain dicts. Use 'type' as a convention:
event = {
    'type': 'payment_processed',
    'payment_id': 'PAY123',
    'amount_cents': 10000,
    'timestamp': '2026-07-07T10:00:00Z',
    'account_id': 'ACC001',
}

publish(event)
```

---

## 🧪 Test Coverage

This kata includes 19 comprehensive tests organized into 6 test classes:

**Subscription Tests (1)**
- Registering and calling handlers

**Publishing Tests (4)**
- Publishing with no subscribers
- Calling all subscribers
- Exception handling and propagation
- Handler exception stops subsequent handlers

**Event Types Tests (2)**
- Events with multiple fields
- 'type' field is convention, not requirement

**Multiple Handlers (1)**
- Handlers called in registration order

**Clear Tests (2)**
- Clearing all subscribers
- Re-subscribing after clear

**Domain Scenarios (9)**
- Account projection simulation
- Multiple projections on same event
- Decoupling domain from side effects
- CQRS read-model pattern
- Audit log pattern

Run tests to see all patterns in action:

```bash
pytest tests/test_message_bus.py -v
```

---

## 🔗 Related Patterns

- **Domain Model** (`../domain_model/`) — Domain objects publish events
- **Service Layer** (`../service_layer/`) — Services coordinate events and business logic
- **Event Sourcing** — Store every event; replay them to rebuild state (advanced)
- **CQRS** (Command Query Responsibility Segregation) — Separate write and read models via events
- **Saga** — Long-running transactions orchestrated via events (advanced)

---

## 📚 Learning Path

1. **Start here**: Understand subscribe/publish as decoupling
2. **Study handlers**: See how handlers react independently to events
3. **Explore ordering**: Observe that handlers are called in subscription order
4. **Try exceptions**: See what happens when a handler fails
5. **Build a projection**: Create a read model that reacts to multiple events
6. **Next kata**: Move to Domain Model and Service Layer to see where events originate

---

## 🎯 Key Takeaways

1. **Message Bus decouples domain from reactions** — Domain publishes events; handlers listen
2. **Handlers are independent** — Each handler has no idea other handlers exist
3. **Synchronous in this kata** — Production buses are usually async (Kafka, RabbitMQ)
4. **Events are plain dicts** — Simple, easy to serialize, language-agnostic contract
5. **This bus is not durable** — Events are lost on restart (use a broker for durability)

---

## 📝 Notes

- **Synchronous processing**: Handlers run in-process and block. Production systems use message brokers for asynchronous, durable messaging.
- **Event structure**: There's no schema enforcement. Use conventions (e.g., 'type' field) so handlers know what events look like.
- **Handler order matters**: Handlers are called in subscription order. If handler A depends on handler B's side effects, register B first.
- **Exception propagation**: If a handler raises, the exception stops other handlers and propagates to the publisher.
- **No event persistence**: Events are not stored. Each publish is processed immediately and discarded.

---

## ⚠️ Important: This Is a Toy Implementation

This Message Bus is simple and educational. For production, consider:

```python
# ❌ This bus (toy implementation):
- Events are lost on restart
- Handlers run synchronously (blocks the publisher)
- No error recovery or retries
- No event ordering guarantees
- Single process only

# ✅ Production message brokers (Kafka, RabbitMQ, etc.):
- Durable event storage
- Async, non-blocking processing
- Dead-letter queues for failed handlers
- Ordering guarantees
- Cross-service communication
```

---

**Next Steps:** After understanding Message Bus, explore `Domain Model` (where events originate) or `Service Layer` (which orchestrates events), or move to a real message broker like Kafka or RabbitMQ for production-grade event-driven systems.
