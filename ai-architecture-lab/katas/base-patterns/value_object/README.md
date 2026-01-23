# Value Object Pattern Kata

A hands-on demonstration of the **Value Object** pattern from PoEAA (Patterns of Enterprise Application Architecture).

---

## 🌱 What Is a Value Object?

A **Value Object** is a small, immutable object whose equality is based on **value**, not identity. Two value objects are equal if they have the same values, regardless of whether they are the same instance.

### Key Characteristics

- ✅ **Immutability**: Once created, cannot be modified
- ✅ **Equality by value**: Two objects with same values are equal
- ✅ **No identity**: Value objects don't have a unique identifier
- ✅ **Self-validating**: Constructor validates and ensures invariants

### Examples

- **Money**: `Money(100, "USD")` - amount and currency
- **Email**: `Email("user@example.com")` - validated email address
- **DateRange**: `DateRange(start, end)` - date range with business logic
- **Address**: `Address(street, city, zip)` - postal address
- **Color**: `Color(255, 0, 0)` - RGB color value

---

## 🎓 Why Use Value Objects?

### Benefits

1. **Prevents bugs**: Immutability prevents accidental modifications
2. **Clear semantics**: Value equality is intuitive (two $10 bills are equal)
3. **Thread-safe**: Immutable objects are naturally thread-safe
4. **Self-documenting**: The type system documents what values are valid
5. **Encapsulates validation**: Business rules live with the data

### When to Use

- ✅ Small, simple objects (1-5 attributes)
- ✅ Objects that represent a "value" (money, email, date range)
- ✅ Objects where equality is based on all attributes
- ✅ Objects that should be immutable

### When NOT to Use

- ❌ Objects with identity (entities, aggregates)
- ❌ Objects that need to change over time
- ❌ Large, complex objects (use entities instead)

---

## 📁 Structure

```
value_object/
├── value_object.py          # Base ValueObject class
├── examples/
│   ├── email.py             # Email value object example
│   └── date_range.py        # DateRange value object example
├── tests/
│   ├── test_value_object.py # Tests for base class
│   ├── test_email.py        # Tests for Email
│   └── test_date_range.py   # Tests for DateRange
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ai-architecture-lab/katas/base-patterns/value_object
pip install -r requirements.txt
```

### 2. Run Tests

```bash
# Run all tests (recommended - this is all you need!)
pytest -v

# Run specific test file
pytest tests/test_email.py -v

# Note: Coverage reports are optional and require pytest-cov
# If you want coverage, install it first: pip install pytest-cov
# Then run: pytest --cov=. --cov-report=html
# But basic testing works perfectly without coverage!
```

### 3. Explore the Code

Start with:
1. `value_object.py` - Base class implementation
2. `examples/email.py` - Simple Email example
3. `examples/date_range.py` - DateRange with business logic
4. `tests/` - Comprehensive test suite

---

## 💡 Usage Examples

### Email Value Object

```python
from examples.email import Email

# Create email (validated automatically)
email1 = Email("user@example.com")
email2 = Email("USER@EXAMPLE.COM")  # Normalized to lowercase

# Value equality
assert email1 == email2  # True - same value

# Use in sets/dicts
email_set = {email1, email2}  # Only one item (they're equal)
email_dict = {email1: "primary"}

# Immutability
print(email1.address)  # "user@example.com"
# email1.address = "new@example.com"  # Error - no setter
```

### DateRange Value Object

```python
from datetime import date
from examples.date_range import DateRange

# Create date range (validated: start <= end)
range1 = DateRange(date(2024, 1, 1), date(2024, 1, 31))
range2 = DateRange(date(2024, 1, 1), date(2024, 1, 31))

# Value equality
assert range1 == range2  # True - same dates

# Business logic
assert range1.contains(date(2024, 1, 15))  # True
assert range1.duration_days() == 31  # 31 days

# Overlap detection
range3 = DateRange(date(2024, 1, 15), date(2024, 2, 15))
assert range1.overlaps(range3)  # True
```

---

## 🧪 Test Coverage

This kata includes comprehensive tests demonstrating:

- ✅ Value-based equality
- ✅ Hash support (for sets/dicts)
- ✅ Immutability
- ✅ Validation
- ✅ Business logic methods
- ✅ String representation

Run tests to see all examples in action:

```bash
pytest -v
```

---

## 🔗 Related Patterns

- **Money**: Specialized Value Object (see `katas/base-patterns/money/`)
- **Entity**: Objects with identity (opposite of Value Object)
- **Special Case**: Null Object variant (see `katas/base-patterns/special_case/`)

---

## 📚 Learning Path

1. **Start here**: Understand the base `ValueObject` class
2. **Study examples**: See `Email` and `DateRange` implementations
3. **Run tests**: Understand behavior through test cases
4. **Try it yourself**: Create your own Value Object (e.g., `PhoneNumber`, `Address`)
5. **Next kata**: Move to `Money` kata (uses Value Object)

---

## 🎯 Key Takeaways

1. **Value Objects are immutable** - Once created, they don't change
2. **Equality is by value** - Two objects with same values are equal
3. **Self-validating** - Constructor ensures invariants
4. **Can be used in collections** - Hash support allows use in sets/dicts
5. **Encapsulate business logic** - Methods like `contains()`, `overlaps()` live with the data

---

## 💻 Creating Your Own Value Object

To create a new Value Object:

1. **Extend `ValueObject`**:
```python
from value_object import ValueObject

class MyValueObject(ValueObject):
    def __init__(self, value: str):
        # Validate and store
        if not value:
            raise ValueError("Value cannot be empty")
        self._value = value
    
    @property
    def value(self) -> str:
        return self._value
    
    def _get_equality_components(self) -> tuple:
        return (self._value,)
```

2. **Add business logic** (optional):
```python
def is_valid(self) -> bool:
    return len(self._value) > 0
```

3. **Write tests**:
```python
def test_equality():
    obj1 = MyValueObject("test")
    obj2 = MyValueObject("test")
    assert obj1 == obj2
```

---

## 📝 Notes

- Python doesn't enforce immutability at the language level
- The pattern encourages immutability through:
  - Private attributes (`_value`)
  - Read-only properties
  - No setter methods
- For production, consider using `@dataclass(frozen=True)` or `attrs` library

---

**Next Steps:** After understanding Value Objects, move to the `Money` kata which demonstrates a specialized Value Object for financial calculations.
