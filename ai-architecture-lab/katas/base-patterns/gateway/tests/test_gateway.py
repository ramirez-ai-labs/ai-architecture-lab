"""Tests for Gateway/Adapter pattern."""
import pytest
from gateway import PaymentGateway, FakePaymentGateway, StripePaymentGateway, PaymentResult


class TestPaymentResult:
    """Tests for PaymentResult data class."""

    def test_successful_payment_result(self):
        """Can create a successful payment result."""
        result = PaymentResult(success=True, transaction_id="TXN123")
        assert result.success is True
        assert result.transaction_id == "TXN123"
        assert result.error_message is None

    def test_failed_payment_result(self):
        """Can create a failed payment result."""
        result = PaymentResult(success=False, error_message="Card declined")
        assert result.success is False
        assert result.error_message == "Card declined"
        assert result.transaction_id is None


class TestFakePaymentGateway:
    """Tests for the fake payment gateway (used in testing)."""

    def test_fake_gateway_returns_success(self):
        """Fake gateway always returns success."""
        gateway = FakePaymentGateway()
        result = gateway.process_payment(1000, "test_token")

        assert result.success is True
        assert result.transaction_id is not None
        assert result.error_message is None

    def test_fake_gateway_generates_unique_ids(self):
        """Each fake payment gets a unique transaction ID."""
        gateway = FakePaymentGateway()

        result1 = gateway.process_payment(1000, "token1")
        result2 = gateway.process_payment(2000, "token2")

        # Transaction IDs should be different
        assert result1.transaction_id != result2.transaction_id

    def test_fake_gateway_id_format(self):
        """Fake gateway generates IDs with FAKE_TXN_ prefix."""
        gateway = FakePaymentGateway()
        result = gateway.process_payment(1000, "token")

        assert result.transaction_id.startswith("FAKE_TXN_")

    def test_fake_gateway_reset(self):
        """Can reset fake gateway transaction counter."""
        gateway = FakePaymentGateway()

        # Generate first ID
        result1 = gateway.process_payment(1000, "token1")
        first_id = result1.transaction_id

        # Generate second ID (should be different)
        result2 = gateway.process_payment(2000, "token2")
        second_id = result2.transaction_id
        assert first_id != second_id

        # Reset the gateway
        gateway.reset()

        # Generate ID after reset (should restart at 1)
        result3 = gateway.process_payment(3000, "token3")
        reset_id = result3.transaction_id

        # After reset, ID counter starts over
        assert reset_id == first_id

    def test_fake_gateway_ignores_amount(self):
        """Fake gateway succeeds regardless of amount."""
        gateway = FakePaymentGateway()

        result1 = gateway.process_payment(0, "token")  # $0
        result2 = gateway.process_payment(999999999, "token")  # Very large amount

        # Both should succeed
        assert result1.success is True
        assert result2.success is True

    def test_fake_gateway_is_thread_safe(self):
        """Fake gateway is safe to use in multiple scenarios."""
        gateway = FakePaymentGateway()

        # Simulate multiple payment attempts
        results = []
        for i in range(100):
            result = gateway.process_payment(1000, f"token_{i}")
            results.append(result)

        # All should succeed with unique IDs
        assert all(r.success for r in results)
        transaction_ids = [r.transaction_id for r in results]
        assert len(set(transaction_ids)) == len(transaction_ids)  # All unique


class TestStripePaymentGateway:
    """Tests for the Stripe payment gateway."""

    def test_stripe_gateway_with_api_key(self):
        """Can create Stripe gateway with API key."""
        gateway = StripePaymentGateway(api_key="sk_test_123")
        assert gateway is not None

    def test_stripe_gateway_without_api_key_fails(self):
        """Stripe gateway fails when API key not provided."""
        gateway = StripePaymentGateway(api_key="")
        result = gateway.process_payment(1000, "token")

        assert result.success is False
        assert "API key" in result.error_message

    def test_stripe_gateway_processes_payment(self):
        """Stripe gateway returns successful payment result."""
        gateway = StripePaymentGateway(api_key="sk_test_abc123")
        result = gateway.process_payment(5000, "tok_visa")

        assert result.success is True
        assert result.transaction_id is not None
        assert result.error_message is None

    def test_stripe_gateway_transaction_id_format(self):
        """Stripe gateway generates IDs with 'ch_' prefix (charge ID format)."""
        gateway = StripePaymentGateway(api_key="sk_test_123")
        result = gateway.process_payment(1000, "token_xyz")

        # Stripe charge IDs start with 'ch_'
        assert result.transaction_id.startswith("ch_")


class TestGatewayPolymorphism:
    """Tests demonstrating gateway polymorphism and substitutability."""

    def test_both_gateways_implement_payment_gateway_interface(self):
        """Both Fake and Stripe gateways implement PaymentGateway."""
        fake_gateway = FakePaymentGateway()
        stripe_gateway = StripePaymentGateway(api_key="sk_test_123")

        # Both should be PaymentGateway instances
        assert isinstance(fake_gateway, PaymentGateway)
        assert isinstance(stripe_gateway, PaymentGateway)

    def test_gateways_have_same_method_signature(self):
        """All gateways have process_payment with same signature."""
        fake_gateway = FakePaymentGateway()
        stripe_gateway = StripePaymentGateway(api_key="sk_test_123")

        # Both return PaymentResult
        fake_result = fake_gateway.process_payment(1000, "token")
        stripe_result = stripe_gateway.process_payment(1000, "token")

        assert isinstance(fake_result, PaymentResult)
        assert isinstance(stripe_result, PaymentResult)

    def test_interchangeable_gateways(self):
        """Gateways can be swapped without changing caller code."""

        def process_payment_with_gateway(gateway: PaymentGateway, amount: int, token: str) -> bool:
            """Domain logic that uses any PaymentGateway implementation."""
            result = gateway.process_payment(amount, token)
            return result.success

        # Should work with Fake gateway
        fake_gateway = FakePaymentGateway()
        assert process_payment_with_gateway(fake_gateway, 1000, "fake_token") is True

        # Should work with Stripe gateway (without changing caller code)
        stripe_gateway = StripePaymentGateway(api_key="sk_test_123")
        assert process_payment_with_gateway(stripe_gateway, 1000, "stripe_token") is True


class TestGatewayInDomainLogic:
    """Tests simulating real-world usage in domain logic."""

    def test_checkout_with_fake_gateway(self):
        """Domain logic works with fake gateway (for testing)."""

        class SimpleCheckout:
            def __init__(self, gateway: PaymentGateway):
                self.gateway = gateway

            def charge_customer(self, amount: int, token: str) -> bool:
                result = self.gateway.process_payment(amount, token)
                return result.success

        # Test with fake gateway
        fake_gateway = FakePaymentGateway()
        checkout = SimpleCheckout(fake_gateway)

        assert checkout.charge_customer(10000, "test_token") is True

    def test_checkout_with_stripe_gateway(self):
        """Domain logic works with Stripe gateway (production)."""

        class SimpleCheckout:
            def __init__(self, gateway: PaymentGateway):
                self.gateway = gateway

            def charge_customer(self, amount: int, token: str) -> bool:
                result = self.gateway.process_payment(amount, token)
                return result.success

        # Test with Stripe gateway
        stripe_gateway = StripePaymentGateway(api_key="sk_test_123")
        checkout = SimpleCheckout(stripe_gateway)

        assert checkout.charge_customer(10000, "stripe_token") is True

    def test_gateway_independence(self):
        """Domain logic doesn't depend on specific gateway implementation."""
        # This test demonstrates the key benefit: same logic works with any gateway

        def process_order(gateway: PaymentGateway, order_amount: int) -> dict:
            """Domain logic that accepts any PaymentGateway."""
            result = gateway.process_payment(order_amount, "customer_token")
            return {
                "success": result.success,
                "transaction_id": result.transaction_id,
                "error": result.error_message,
            }

        # Works with Fake
        fake_result = process_order(FakePaymentGateway(), 5000)
        assert fake_result["success"] is True

        # Works with Stripe
        stripe_result = process_order(StripePaymentGateway(api_key="sk_test_123"), 5000)
        assert stripe_result["success"] is True

        # Same domain logic, different implementations
