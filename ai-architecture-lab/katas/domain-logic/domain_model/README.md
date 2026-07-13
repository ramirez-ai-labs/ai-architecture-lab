# Domain Model Kata

## Overview

This kata teaches you how to build **rich domain objects** that encapsulate business logic and behavior, rather than using transaction scripts where logic lives in HTTP handlers or service functions.

## Learning Objectives

- ✅ Understand the difference between domain entities and data containers
- ✅ Encapsulate business rules within domain objects
- ✅ Build domain models that are framework-agnostic (no FastAPI, Flask, etc.)
- ✅ Write unit tests for business logic without infrastructure dependencies
- ✅ See how domain objects enable code reuse across different contexts (web, CLI, AI pipelines)

## Concepts

### Message
A simple domain entity representing a single chat message:
- `sender` - who sent the message
- `text` - message content
- `created_at` - timestamp (automatically set)

### Conversation
A rich domain object representing a collection of messages with behavior:
- `id` - optional database identifier
- `title` - conversation name
- `messages` - list of Message objects
- `closed` - whether the conversation accepts new messages

**Key Behavior:**
- **add_message()** - enforces the rule: "cannot add messages to closed conversations"
- **message_count()** - returns number of messages
- **total_word_count()** - counts words across all messages
- **last_message()** - retrieves the most recent message
- **close()** - marks conversation as complete

## File Structure

```
domain_model/
├── __init__.py              # Package initialization
├── domain.py                # Core domain entities
├── README.md                # This file
├── requirements.txt         # Dependencies
├── examples/
│   ├── __init__.py
│   └── basic_conversation.py
└── tests/
    ├── __init__.py
    └── test_domain.py
```

## Getting Started

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Examples
```bash
python examples/basic_conversation.py
```

### Run Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=domain --cov-report=html
```

## Key Takeaways

1. **Domain objects encapsulate behavior** - they're not just data containers
2. **Business rules live in the domain layer** - not in HTTP handlers or databases
3. **Domain models are framework-agnostic** - can be used anywhere
4. **Easy to test** - no database, no web framework needed
5. **Reusable** - same logic works for web APIs, CLIs, AI pipelines, jobs

## Related Katas

- **Service Layer** - How to coordinate multiple domain objects
- **Repository** - How to persist domain objects
- **Value Objects** - Similar to domain entities but immutable
