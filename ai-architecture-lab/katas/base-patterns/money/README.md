# Money Pattern Kata

A specialized **Value Object** for representing monetary amounts with currency, demonstrating precision-safe financial calculations.

---

## 🌱 What Is Money as a Value Object?

**Money** is a specialized Value Object that represents monetary amounts with currency. It extends the Value Object pattern to handle the unique requirements of financial calculations:

- ✅ **Precision-safe**: Uses integer cents (no floating point!)
- ✅ **Currency-aware**: Tracks currency code (USD, EUR, GBP, etc.)
- ✅ **Immutable**: Once created, cannot be modified
- ✅ **Arithmetic operations**: add, subtract, multiply
- ✅ **Value equality**: Two Money objects with same amount and currency are equal

### Why No Floating Point?

Floating point arithmetic has precision errors that are unacceptable for money:

```python
# ❌ BAD: Floating point precision error
0.1 + 0.2  # = 0.30000000000000004 (wrong!)

# ✅ GOOD: Integer cents (no precision error)
Money(10, "USD").add(Money(20, "USD"))  # = $0.30 (correct!)
```

**Solution**: Store amounts as integer cents (100 cents = $1.00)

---

## 🎓 Why Use Money Value Object?

### Benefits

1. **Prevents precision errors**: Integer arithmetic is exact
2. **Currency safety**: Cannot accidentally mix currencies
3. **Immutable**: Prevents accidental modifications
4. **Self-validating**: Constructor ensures valid amounts and currencies
5. **Clear semantics**: `Money(1000, "USD")` is clearer than `10.00`

### When to Use

- ✅ Financial calculations (prices, payments, balances)
- ✅ Currency-aware applications
- ✅ Anywhere precision matters (accounting, banking)
- ✅ Multi-currency systems

### When NOT to Use

- ❌ Simple numeric calculations (use `float` or `Decimal`)
- ❌ Non-financial amounts (use regular numbers)
- ❌ When you need mutable amounts (use a different pattern)

---

## 📁 Structure

```
money/
├── money.py                    # Money value object implementation
├── examples/
│   └── currency_conversion.py # Currency conversion example
├── tests/
│   ├── test_money.py          # Tests for Money
│   └── test_currency_conversion.py  # Tests for conversion
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ai-architecture-lab/katas/base-patterns/money
pip install -r requirements.txt
```

### 2. Run Tests

```bash
# Run all tests (recommended)
pytest -v

# Run specific test file
pytest tests/test_money.py -v
```

### 3. Explore the Code

Start with:
1. `money.py` - Money class implementation
2. `examples/currency_conversion.py` - Currency conversion example
3. `tests/` - Comprehensive test suite

---

## 💡 Usage Examples

### Basic Money Operations

```python
from money import Money

# Create money (amount in cents)
money1 = Money(1000, "USD")  # $10.00
money2 = Money(500, "USD")   # $5.00

# Arithmetic operations
total = money1.add(money2)        # $15.00
difference = money1.subtract(money2)  # $5.00
doubled = money1.multiply(2.0)    # $20.00

# Business logic
print(money1.is_zero())      # False
print(money1.is_positive())  # True
```

### Currency Handling

```python
# Different currencies
usd_money = Money(1000, "USD")  # $10.00
eur_money = Money(1000, "EUR")  # €10.00

# Cannot mix currencies
try:
    usd_money.add(eur_money)  # Raises ValueError
except ValueError as e:
    print(e)  # "Currencies must match"
```

### Precision Safety

```python
# No floating point precision errors!
money1 = Money(10, "USD")   # $0.10
money2 = Money(20, "USD")   # $0.20

total = money1.add(money2)
print(total)  # "$0.30" (exactly, no precision error!)

# Compare to floating point:
# 0.1 + 0.2 = 0.30000000000000004 (wrong!)
```

### Currency Conversion

```python
from examples.currency_conversion import convert_currency

usd_money = Money(1000, "USD")  # $10.00

# Convert to EUR
eur_money = convert_currency(usd_money, "EUR")
print(eur_money)  # €8.50 (using exchange rate)
```

---

## 🧪 Test Coverage

This kata includes comprehensive tests demonstrating:

- ✅ Money creation and validation
- ✅ Currency handling and validation
- ✅ Precision rules (integer cents, no floating point)
- ✅ Arithmetic operations (add, subtract, multiply)
- ✅ Value-based equality
- ✅ Immutability
- ✅ Currency conversion
- ✅ Business logic methods (is_zero, is_positive)

Run tests to see all examples in action:

```bash
pytest -v
```

---

## 🔗 Related Patterns

- **Value Object**: Base pattern that Money extends (see `../value_object/`)
- **Entity**: Objects with identity (opposite of Value Object)
- **Table Data Gateway**: May use Money for financial data

---

## 📚 Learning Path

1. **Start here**: Understand how Money extends Value Object
2. **Study precision**: See why integers are used instead of floats
3. **Try arithmetic**: Experiment with add, subtract, multiply
4. **Explore currency**: See how currencies are handled
5. **Next kata**: Move to Table Data Gateway (uses Money for financial data)

---

## 🎯 Key Takeaways

1. **Money uses integers** - Store cents, not dollars (prevents precision errors)
2. **Currency is part of equality** - $10 USD ≠ €10 EUR
3. **Operations return new objects** - Money is immutable
4. **Currency mixing is prevented** - Cannot add USD to EUR
5. **Self-validating** - Constructor ensures valid amounts and currencies

---

## 💻 Creating Money Objects

### From Dollars to Cents

```python
# Convert dollars to cents
dollars = 10.50
cents = int(dollars * 100)  # 1050 cents

money = Money(cents, "USD")
print(money)  # "$10.50"
```

### Common Amounts

```python
# $0.01 (1 cent)
penny = Money(1, "USD")

# $1.00 (100 cents)
dollar = Money(100, "USD")

# $10.00 (1000 cents)
ten_dollars = Money(1000, "USD")
```

---

## 📝 Notes

- **Precision**: Always use integer cents. Never use `float` for money!
- **Currency codes**: Uses ISO 4217 codes (USD, EUR, GBP, JPY, etc.)
- **Rounding**: Multiplication rounds to nearest cent
- **Immutability**: All operations return new Money objects
- **Currency conversion**: Example shows simplified conversion (production would use live rates)

---

## ⚠️ Important: Floating Point Precision

**Never use floating point for money!**

```python
# ❌ BAD: Floating point
price = 10.50
tax = price * 0.08  # Might have precision errors!

# ✅ GOOD: Money with integers
price = Money(1050, "USD")  # $10.50
tax = price.multiply(0.08)  # Exact calculation
```

---

**Next Steps:** After understanding Money, move to the `Table Data Gateway` kata which can use Money for financial data storage.
