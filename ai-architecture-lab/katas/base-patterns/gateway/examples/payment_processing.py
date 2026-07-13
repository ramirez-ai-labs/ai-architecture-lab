"""Example: Payment processing with swappable payment gateways.

SCENARIO:
We're building an e-commerce checkout system. We need to process payments.
Instead of calling Stripe directly, we use a gateway to stay flexible.

THIS EXAMPLE DEMONSTRATES:
1. Domain logic using a payment gateway (decoupled)
2. Swapping between fake and real implementations
3. Testing without touching real payment systems
4. How to handle payment failures
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from gateway import FakePaymentGateway, StripePaymentGateway, PaymentGateway


class CheckoutService:
    """Service that processes orders using a payment gateway.

    WHAT IS THIS?
    This is domain logic (your business logic) that uses a payment gateway.
    Notice: it doesn't know or care whether it's using Fake or Stripe.
    The gateway is injected (dependency injection pattern).
    """

    def __init__(self, payment_gateway: PaymentGateway):
        """Initialize checkout service with a payment gateway.

        Args:
            payment_gateway: Any PaymentGateway implementation
        """
        self.payment_gateway = payment_gateway

    def process_order(self, order_id: str, amount_cents: int, payment_token: str) -> bool:
        """Process an order by charging the customer.

        WHAT DOES THIS DO?
        1. Takes an order and payment details
        2. Calls the payment gateway to process the payment
        3. Logs the result
        4. Returns success/failure

        NOTE: This doesn't depend on any specific payment processor.
        Works with FakePaymentGateway, StripePaymentGateway, or any
        other implementation of PaymentGateway.

        Args:
            order_id: Unique order identifier
            amount_cents: Order amount in cents
            payment_token: Payment method token

        Returns:
            True if payment succeeded, False otherwise
        """
        # Use the injected gateway to process the payment
        result = self.payment_gateway.process_payment(amount_cents, payment_token)

        # Log the transaction
        if result.success:
            print(f"Order {order_id}: Payment succeeded (txn {result.transaction_id})")
        else:
            print(f"Order {order_id}: Payment failed - {result.error_message}")

        return result.success


def main():
    """Run the payment processing example."""

    print("=== Payment Gateway Pattern Example ===\n")

    # =========================================================================
    # SCENARIO 1: Testing with Fake Gateway
    # =========================================================================
    print("--- SCENARIO 1: Testing with Fake Gateway ---\n")

    # Create a fake gateway (perfect for testing)
    fake_gateway = FakePaymentGateway()

    # Create checkout service with the fake gateway
    test_checkout = CheckoutService(fake_gateway)

    # Process an order using the fake gateway
    print("Processing order with fake payment gateway:")
    success = test_checkout.process_order("ORDER001", 10000, "test_token_123")
    print(f"Result: {'SUCCESS' if success else 'FAILED'}\n")

    # =========================================================================
    # SCENARIO 2: Testing payment failure
    # =========================================================================
    print("--- SCENARIO 2: Simulating Multiple Test Cases ---\n")

    print("Processing 3 test orders:")
    for i in range(1, 4):
        order_id = f"ORDER{i:03d}"
        amount = 5000 + (i * 1000)  # $50, $60, $70
        token = f"token_{i}"

        result = fake_gateway.process_payment(amount, token)
        status = "[OK] Success" if result.success else "[FAIL] Failed"
        print(f"  {order_id}: {status} (Transaction: {result.transaction_id})")

    print()

    # =========================================================================
    # SCENARIO 3: Production with Stripe Gateway
    # =========================================================================
    print("--- SCENARIO 3: Production with Stripe Gateway ---\n")

    # In production, you'd use the real Stripe gateway
    stripe_gateway = StripePaymentGateway(api_key="sk_test_abc123")

    # Create checkout service with Stripe gateway
    production_checkout = CheckoutService(stripe_gateway)

    # IMPORTANT: The checkout service code doesn't change!
    # It works the same way with both Fake and Stripe gateways
    print("Processing order with Stripe payment gateway:")
    success = production_checkout.process_order("ORDER100", 15000, "stripe_token_xyz")
    print(f"Result: {'SUCCESS' if success else 'FAILED'}\n")

    # =========================================================================
    # SCENARIO 4: Why This Pattern Matters
    # =========================================================================
    print("--- SCENARIO 4: Why This Pattern Matters ---\n")

    print("KEY BENEFITS:\n")

    print("1. TESTABILITY:")
    print("   - Use FakePaymentGateway in unit tests")
    print("   - No network calls, no external dependencies")
    print("   - Tests are fast and reliable\n")

    print("2. FLEXIBILITY:")
    print("   - Want to switch from Stripe to PayPal? Create PayPalGateway class")
    print("   - CheckoutService doesn't change (still uses PaymentGateway interface)")
    print("   - Just inject the new gateway\n")

    print("3. DECOUPLING:")
    print("   - CheckoutService doesn't know about Stripe API details")
    print("   - Stripe API changes don't break your domain logic")
    print("   - Payment provider is swappable\n")

    print("4. ISOLATION:")
    print("   - External system failures are isolated")
    print("   - Easy to add logging/monitoring at gateway level")
    print("   - Central place to handle retries, rate limiting, etc.\n")

    # =========================================================================
    # SCENARIO 5: Multiple Gateways in Same Application
    # =========================================================================
    print("--- SCENARIO 5: Multiple Gateways for Different Contexts ---\n")

    # Use fake gateway for development/testing
    dev_gateway = FakePaymentGateway()
    dev_checkout = CheckoutService(dev_gateway)

    # Use Stripe gateway for production
    prod_gateway = StripePaymentGateway(api_key="sk_live_real_key")
    prod_checkout = CheckoutService(prod_gateway)

    print("Development environment: Using FakePaymentGateway")
    dev_checkout.process_order("DEV001", 1000, "dev_token")

    print("\nProduction environment: Using StripePaymentGateway")
    prod_checkout.process_order("PROD001", 1000, "prod_token")

    print("\n=== Payment Gateway Example Complete ===")


if __name__ == "__main__":
    main()
