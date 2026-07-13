# Gateway/Adapter Pattern Kata

Wrapping external systems behind a stable, internal interface.

---

## 🌱 What Is a Gateway?

**Gateway** (also called Adapter) is an object that encapsulates access to an external system. Instead of calling an external API directly, you wrap it behind a stable interface that your code depends on.

### Problem Without Gateway

```python
# Your code directly depends on Stripe API
def process_payment(amount_cents, card_token):
    stripe_response = stripe.Charge.create(
        amount=amount_cents,
        currency="usd",
        source=card_token,
    )
    return stripe_response.id

# Problems:
# - Tightly coupled to Stripe's API
# - Can't test without calling Stripe
# - If you switch providers, you must rewrite everything
```

### Solution With Gateway

```python
class PaymentGateway:  # Abstract interface
    def process_payment(self, amount_cents, token) -> PaymentResult:
        pass

class StripePaymentGateway(PaymentGateway):  # Stripe implementation
    def process_payment(self, amount_cents, token):
        # Stripe-specific logic here
        pass

# Your code depends on the interface, not Stripe
def process_order(gateway: PaymentGateway, amount, token):
    result = gateway.process_payment(amount, token)
    return result

# Now you can swap providers without changing domain logic
```

---

## 🎓 Why Use Gateways?

### Benefits

1. **Decoupling**: Your code doesn't depend on external system APIs
2. **Testability**: Easy to create fake implementations for testing
3. **Flexibility**: Swap providers (Stripe → PayPal) without rewriting logic
4. **Isolation**: External system changes don't affect your code
5. **Centralization**: All external system logic in one place

### When to Use

- ✅ Payment processors (Stripe, PayPal, Square)
- ✅ Email services (SendGrid, Mailgun)
- ✅ SMS providers (Twilio)
- ✅ Cloud storage (AWS S3, Google Cloud Storage)
- ✅ External APIs (any third-party service)

### When NOT to Use

- ❌ Internal services (use direct calls or microservice communication)
- ❌ Simple libraries (no need to wrap everything)

---

## 📁 Structure

```
gateway/
├── gateway.py                  # PaymentGateway interface, implementations
├── examples/
│   └── payment_processing.py  # Example: swappable payment gateways
├── tests/
│   └── test_gateway.py        # 18 comprehensive tests
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ai-architecture-lab/katas/base-patterns/gateway
pip install -r requirements.txt
```

### 2. Run Tests

```bash
pytest -v
```

### 3. Run Example

```bash
python examples/payment_processing.py
```

---

## 💡 Usage Examples

### Creating Gateways

```python
from gateway import FakePaymentGateway, StripePaymentGateway

# For testing
test_gateway = FakePaymentGateway()

# For production
prod_gateway = StripePaymentGateway(api_key="sk_live_123")
```

### Using in Domain Logic

```python
class CheckoutService:
    def __init__(self, payment_gateway: PaymentGateway):
        # Inject the gateway (dependency injection)
        self.gateway = payment_gateway

    def process_order(self, order_id, amount_cents, token):
        # Call gateway without knowing which implementation
        result = self.gateway.process_payment(amount_cents, token)

        if result.success:
            print(f"Order {order_id}: Success (ID: {result.transaction_id})")
        else:
            print(f"Order {order_id}: Failed - {result.error_message}")

        return result.success
```

### Testing with Fake Gateway

```python
def test_successful_checkout():
    # Use fake gateway (no network calls)
    gateway = FakePaymentGateway()
    checkout = CheckoutService(gateway)

    # Test your logic
    success = checkout.process_order("ORDER1", 1000, "token")
    assert success is True
```

### Production with Stripe

```python
def main():
    # Use real gateway in production
    gateway = StripePaymentGateway(api_key=os.getenv("STRIPE_KEY"))
    checkout = CheckoutService(gateway)

    # Same code, different implementation
    checkout.process_order("ORDER1", 1000, "stripe_token")
```

---

## 🧪 Test Coverage

This kata includes **18 comprehensive tests** organized into 6 test classes:

**PaymentResult Tests (2)**
- Successful payment result
- Failed payment result

**Fake Gateway Tests (6)**
- Always returns success
- Generates unique transaction IDs
- ID format validation
- Transaction counter reset
- Ignores amount (for testing)
- Thread-safe behavior

**Stripe Gateway Tests (4)**
- Creating with API key
- Failing without API key
- Processing payment
- Transaction ID format

**Polymorphism Tests (3)**
- Both gateways implement interface
- Same method signature
- Interchangeable implementations

**Domain Logic Tests (3)**
- Works with fake gateway
- Works with Stripe gateway
- Gateway independence

Run tests:

```bash
pytest tests/test_gateway.py -v
```

---

## 🔗 Related Patterns

- **Strategy** — Gateway is a specific use of Strategy pattern (swap algorithms)
- **Adapter** — Converts one interface to another (gateway wraps external API)
- **Facade** — Simplifies complex external system (gateway hides complexity)
- **Dependency Injection** — Inject gateway into services (decouple from implementation)

---

## 📚 Learning Path

1. **Start here**: Understand why wrapping external systems matters
2. **Study the interface**: See how PaymentGateway defines the contract
3. **Compare implementations**: Observe Fake vs Stripe differences
4. **Try swapping**: See how easy it is to change providers
5. **Test with fake**: Build tests using FakePaymentGateway
6. **Next kata**: Use gateways in real services

---

## 🎯 Key Takeaways

1. **Gateway wraps external systems** — Hide complexity behind stable interface
2. **Decouples your code** — Depends on interface, not implementation
3. **Easy to test** — Create fake implementations for unit tests
4. **Easy to swap** — Change providers without rewriting logic
5. **Centralized logic** — All external system logic in one place

---

## 📝 Notes

- **Abstract base class**: Use ABC to enforce interface contract
- **Fake implementation**: Always succeeds for testing
- **Real implementation**: Handles specific external system API
- **Dependency injection**: Pass gateway to services via constructor
- **Error handling**: Return result object, don't raise exceptions

---

**Next Steps:** Use gateways when building services that interact with external systems. Create new gateway implementations for different providers.
