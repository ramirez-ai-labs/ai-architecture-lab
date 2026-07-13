"""Tests for Message Bus pattern."""
import pytest
from message_bus import subscribe, publish, clear


@pytest.fixture(autouse=True)
def cleanup():
    """Clear subscribers before and after each test."""
    clear()
    yield
    clear()


class TestSubscription:
    """Tests for subscription mechanism."""

    def test_can_subscribe_handler(self):
        """Can register a handler."""
        called = []

        def handler(event):
            called.append(event)

        subscribe(handler)
        publish({'type': 'test_event'})
        assert len(called) == 1

    def test_multiple_handlers_called_in_order(self):
        """Multiple handlers are called in registration order."""
        calls = []

        def handler1(event):
            calls.append(('handler1', event['type']))

        def handler2(event):
            calls.append(('handler2', event['type']))

        subscribe(handler1)
        subscribe(handler2)
        publish({'type': 'test'})

        assert calls == [('handler1', 'test'), ('handler2', 'test')]

    def test_handler_receives_event_dict(self):
        """Handler receives the published event dict."""
        received = []

        def handler(event):
            received.append(event)

        subscribe(handler)
        event = {'type': 'account_created', 'account_id': 123}
        publish(event)

        assert len(received) == 1
        assert received[0] == event


class TestPublishing:
    """Tests for publishing events."""

    def test_publish_with_no_subscribers(self):
        """Publishing with no subscribers doesn't raise."""
        publish({'type': 'test'})  # Should not raise

    def test_publish_calls_all_subscribers(self):
        """Publishing calls all registered subscribers."""
        calls = []

        for i in range(3):
            subscribe(lambda e, i=i: calls.append(i))

        publish({'type': 'test'})
        assert len(calls) == 3

    def test_handler_exception_propagates(self):
        """If a handler raises, the exception propagates to caller."""
        def bad_handler(event):
            raise ValueError("Handler error")

        subscribe(bad_handler)

        with pytest.raises(ValueError, match="Handler error"):
            publish({'type': 'test'})

    def test_handler_exception_stops_other_handlers(self):
        """If a handler raises, subsequent handlers are not called."""
        calls = []

        def handler1(event):
            calls.append(1)
            raise ValueError("Handler 1 failed")

        def handler2(event):
            calls.append(2)

        subscribe(handler1)
        subscribe(handler2)

        with pytest.raises(ValueError):
            publish({'type': 'test'})

        # Only handler1 was called
        assert calls == [1]


class TestEventTypes:
    """Tests for event payload handling."""

    def test_event_with_multiple_fields(self):
        """Events can have multiple fields."""
        received = []

        def handler(event):
            received.append(event)

        subscribe(handler)
        event = {
            'type': 'deposit_made',
            'account_id': 'ACC001',
            'amount_cents': 10000,
            'timestamp': '2026-07-07T10:00:00Z',
        }
        publish(event)

        assert received[0] == event

    def test_event_type_field_is_convention_not_requirement(self):
        """Events don't require a 'type' field; it's just a convention."""
        received = []

        def handler(event):
            received.append(event)

        subscribe(handler)
        event = {'some_field': 'some_value'}
        publish(event)

        assert received[0] == event


class TestClear:
    """Tests for clearing subscribers."""

    def test_clear_removes_all_subscribers(self):
        """Clear removes all registered subscribers."""
        calls = []

        subscribe(lambda e: calls.append(1))
        subscribe(lambda e: calls.append(2))

        clear()
        publish({'type': 'test'})

        assert len(calls) == 0

    def test_can_resubscribe_after_clear(self):
        """Can register new subscribers after clearing."""
        calls = []

        subscribe(lambda e: calls.append(1))
        clear()
        subscribe(lambda e: calls.append(2))
        publish({'type': 'test'})

        assert calls == [2]


class TestDomainEventScenarios:
    """Tests simulating domain event scenarios."""

    def test_account_projection_scenario(self):
        """Test a simple account read-model projection."""
        accounts = {}

        def on_account_created(event):
            if event['type'] == 'account_created':
                accounts[event['account_id']] = {
                    'balance': event.get('initial_balance', 0),
                }

        def on_deposit(event):
            if event['type'] == 'deposit_made':
                account_id = event['account_id']
                if account_id in accounts:
                    accounts[account_id]['balance'] += event['amount']

        subscribe(on_account_created)
        subscribe(on_deposit)

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
        assert accounts['ACC001']['balance'] == 1500

    def test_multiple_projections_listening_to_same_event(self):
        """Multiple projections can listen to the same event independently."""
        read_model_accounts = {}
        audit_log = []

        def account_projection(event):
            if event['type'] == 'transfer_completed':
                account_id = event['from_account']
                read_model_accounts[account_id] = event['new_balance']

        def audit_log_projection(event):
            audit_log.append(event['type'])

        subscribe(account_projection)
        subscribe(audit_log_projection)

        publish({
            'type': 'transfer_completed',
            'from_account': 'ACC001',
            'new_balance': 500,
        })

        assert read_model_accounts['ACC001'] == 500
        assert 'transfer_completed' in audit_log

    def test_event_decouples_domain_from_side_effects(self):
        """Publishing an event decouples domain logic from side effects."""
        domain_executed = []
        side_effect_executed = []

        def domain_logic(event):
            domain_executed.append('done')

        def email_notification(event):
            side_effect_executed.append(f'email sent for {event["type"]}')

        subscribe(domain_logic)
        subscribe(email_notification)

        publish({'type': 'user_registered'})

        # Both ran independently
        assert domain_executed == ['done']
        assert len(side_effect_executed) == 1
