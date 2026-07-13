"""Gateway/Adapter pattern for wrapping external systems.

WHAT IS A GATEWAY (OR ADAPTER)?
A Gateway wraps an external system (payment processor, email service, SMS provider)
behind a stable, internal interface. This lets your domain logic work with external
systems without depending on their specific APIs.

BEFORE GATEWAY (tightly coupled to external system):
    # Your code directly calls Stripe API
    def process_payment(amount, card_token):
        stripe_response = stripe.Charge.create(
            amount=amount_cents,
            currency="usd",
            source=card_token,
        )
        return stripe_response.id

    # Problem: Your code is tightly coupled to Stripe's API
    # If you switch payment providers, you must rewrite your code
    # Testing requires mocking Stripe's API

AFTER GATEWAY (decoupled via stable interface):
    class PaymentGateway:
        def process_payment(self, amount_cents, token):
            pass  # Abstract method

    class StripeGateway(PaymentGateway):
        def process_payment(self, amount_cents, token):
            stripe_response = stripe.Charge.create(...)
            return stripe_response.id

    # Your code uses the gateway, not Stripe directly
    def process_payment(gateway: PaymentGateway, amount, token):
        result = gateway.process_payment(amount, token)
        return result

    # Now you can:
    # - Swap payment providers by changing implementations
    # - Test easily with a FakePaymentGateway
    # - Keep your domain logic independent of external APIs

KEY BENEFITS:
1. DECOUPLING: Your code doesn't depend on external system APIs
2. TESTABILITY: Easy to create fake implementations
3. FLEXIBILITY: Swap providers without rewriting domain logic
4. ISOLATION: External system changes don't affect your code
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class PaymentResult:
    """Result of a payment transaction.

    WHAT IS THIS?
    A simple data class representing the outcome of a payment operation.
    It's a DTO (Data Transfer Object) that carries the result across
    the boundary between your domain and the external payment system.

    FIELDS:
    - success: Whether the payment went through
    - transaction_id: Unique ID from the payment processor (for reconciliation)
    - error_message: Human-readable error if payment failed
    """

    success: bool
    transaction_id: Optional[str] = None
    error_message: Optional[str] = None


class PaymentGateway(ABC):
    """Abstract base class defining the payment gateway interface.

    WHAT DOES THIS DO?
    This is the stable, internal interface that your domain logic uses.
    All payment gateways must implement these methods with the same contract.

    WHY ABSTRACT BASE CLASS?
    - Forces all implementations to have the same methods
    - Documents the contract (what methods must exist)
    - Enables polymorphism (swap implementations without changing callers)
    - Makes testing easy (create a fake implementation)

    IMPLEMENTATION PATTERN:
    Concrete gateways (StripePaymentGateway, PayPalGateway, etc.) inherit from
    this class and implement the abstract methods. Each concrete class handles
    the specific details of that external system's API.
    """

    @abstractmethod
    def process_payment(self, amount_cents: int, token: str) -> PaymentResult:
        """Process a payment transaction.

        WHAT IS amount_cents?
        Amount in cents (not dollars) to avoid floating-point precision issues.
        Example: $10.00 is represented as 1000 cents.

        WHAT IS token?
        A secure token representing the customer's payment method
        (credit card, bank account, etc.). The payment processor returns
        a token that you use to charge later without storing sensitive data.

        CONTRACT THAT ALL IMPLEMENTATIONS MUST FOLLOW:
        - Input: amount_cents (positive integer), token (string)
        - Output: PaymentResult with success, transaction_id, error_message
        - Side effects: Contacts external payment system

        IMPORTANT: This method should not raise exceptions.
        Instead, return PaymentResult with success=False and error_message set.
        This makes it easier for callers to handle errors.

        Args:
            amount_cents: Payment amount in cents (must be positive)
            token: Payment token from the payment processor

        Returns:
            PaymentResult with success status and transaction details
        """
        pass


class FakePaymentGateway(PaymentGateway):
    """Fake payment gateway for testing (always succeeds).

    WHAT IS THIS?
    A test double that implements the PaymentGateway interface but doesn't
    contact a real payment processor. Perfect for unit tests.

    WHY USE THIS?
    - No external dependencies (fast tests)
    - No side effects (safe to run anywhere)
    - Controllable behavior (can make it fail if needed)
    - Deterministic (same input always gives same output)

    TESTING PATTERN:
    Use this in your tests instead of the real Stripe gateway:
        def test_checkout():
            gateway = FakePaymentGateway()
            result = gateway.process_payment(1000, "fake_token")
            assert result.success is True
            assert result.transaction_id is not None
    """

    def __init__(self):
        """Initialize the fake gateway.

        WHAT DOES THIS DO?
        Sets up internal state for the fake gateway.
        """
        # Counter to generate unique transaction IDs
        self._transaction_counter = 0

    def process_payment(self, amount_cents: int, token: str) -> PaymentResult:
        """Process a payment (always succeeds).

        WHAT DOES THIS DO?
        Simulates a successful payment without contacting any real system.
        This is perfect for testing.

        BEHAVIOR:
        - Always returns success=True
        - Generates a unique transaction_id (FAKE_TXN_<counter>)
        - No network calls, no side effects

        Args:
            amount_cents: Payment amount in cents (ignored in fake)
            token: Payment token (ignored in fake)

        Returns:
            PaymentResult with success=True and generated transaction_id
        """
        # Increment counter to ensure unique transaction IDs
        self._transaction_counter += 1

        # Generate a fake transaction ID
        fake_transaction_id = f"FAKE_TXN_{self._transaction_counter:06d}"

        # Return successful payment result
        return PaymentResult(
            success=True,
            transaction_id=fake_transaction_id,
            error_message=None,
        )

    def reset(self):
        """Reset the transaction counter (useful between tests)."""
        self._transaction_counter = 0


class StripePaymentGateway(PaymentGateway):
    """Payment gateway for Stripe API.

    WHAT IS THIS?
    A real implementation that contacts the Stripe payment processor.
    This is what you'd use in production (with real Stripe API keys).

    WHY THIS PATTERN?
    - Encapsulates all Stripe-specific logic in one place
    - Your domain code uses the abstract PaymentGateway interface
    - Easy to replace with a different provider
    - Stripe implementation details don't leak into your code

    NOTE: This is a simplified example. Real Stripe integration needs:
    - Error handling for network failures
    - Retry logic for transient failures
    - Webhook handling for asynchronous updates
    - Rate limiting
    - Logging and monitoring
    """

    def __init__(self, api_key: str):
        """Initialize the Stripe gateway.

        WHAT DOES THIS DO?
        Stores the Stripe API key needed to authenticate requests.

        Args:
            api_key: Your Stripe API secret key (in real code, use environment variables)
        """
        # Store the API key for authentication
        # In production, this would come from environment variables, not arguments
        self._api_key = api_key

    def process_payment(self, amount_cents: int, token: str) -> PaymentResult:
        """Process a payment via Stripe.

        WHAT DOES THIS DO?
        Converts our internal contract (amount_cents, token) into Stripe's
        API call format, calls Stripe, and converts the response back to
        our PaymentResult format.

        THIS IS THE TRANSLATION LAYER:
        - Our format ← → Stripe format
        - Our error handling ← → Stripe error handling
        - Our data types ← → Stripe data types

        Args:
            amount_cents: Payment amount in cents
            token: Stripe payment token

        Returns:
            PaymentResult with Stripe transaction details
        """
        # THIS IS PSEUDOCODE - Real Stripe integration would look like:
        # try:
        #     stripe.api_key = self._api_key
        #     charge = stripe.Charge.create(
        #         amount=amount_cents,
        #         currency="usd",
        #         source=token,
        #     )
        #     return PaymentResult(
        #         success=True,
        #         transaction_id=charge.id,
        #     )
        # except stripe.error.CardError as e:
        #     return PaymentResult(
        #         success=False,
        #         error_message=str(e),
        #     )

        # For this kata, we simulate success
        if not self._api_key:
            return PaymentResult(
                success=False,
                error_message="API key not configured",
            )

        # Simulate a successful Stripe charge
        stripe_transaction_id = f"ch_{token[:20]}"  # Simulate Stripe charge ID format

        return PaymentResult(
            success=True,
            transaction_id=stripe_transaction_id,
            error_message=None,
        )
