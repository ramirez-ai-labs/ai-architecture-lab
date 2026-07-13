"""Example: Bank account events coordinated by a message bus.

Simulates a CQRS pattern where a write model publishes domain events
(AccountCreated, DepositMade) and multiple read-model projections listen
and update their own state independently. This decouples the write-side
business logic from the read-side query models.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from message_bus import subscribe, publish, clear


class AccountReadModel:
    """A read-model projection that listens to account events."""

    def __init__(self):
        self.accounts = {}  # account_id -> {'balance_cents': ..., 'created_at': ...}

    def on_account_created(self, event):
        """Handle AccountCreated event."""
        if event['type'] != 'account_created':
            return
        account_id = event['account_id']
        initial_balance = event.get('initial_balance_cents', 0)
        self.accounts[account_id] = {
            'balance_cents': initial_balance,
            'transaction_count': 0,
        }

    def on_deposit_made(self, event):
        """Handle DepositMade event."""
        if event['type'] != 'deposit_made':
            return
        account_id = event['account_id']
        amount = event['amount_cents']
        if account_id in self.accounts:
            self.accounts[account_id]['balance_cents'] += amount
            self.accounts[account_id]['transaction_count'] += 1

    def get_balance(self, account_id):
        """Query the read model for account balance."""
        if account_id not in self.accounts:
            return None
        return self.accounts[account_id]['balance_cents']

    def get_account(self, account_id):
        """Query the read model for full account info."""
        return self.accounts.get(account_id)


class AuditLog:
    """An audit log that records all events for compliance."""

    def __init__(self):
        self.events = []

    def record(self, event):
        """Record an event in the audit log."""
        self.events.append(event)

    def get_events(self):
        """Retrieve all recorded events."""
        return list(self.events)


def main():
    print("=== Bank Account with Message Bus ===\n")

    # Create projections
    read_model = AccountReadModel()
    audit_log = AuditLog()

    # Subscribe to events
    subscribe(read_model.on_account_created)
    subscribe(read_model.on_deposit_made)
    subscribe(audit_log.record)

    print("--- Publishing domain events ---\n")

    # Publish an account creation event
    create_event = {
        'type': 'account_created',
        'account_id': 'ACC001',
        'initial_balance_cents': 50000,  # $500.00
    }
    print(f"Publishing: {create_event}")
    publish(create_event)

    # Query the read model
    balance = read_model.get_balance('ACC001')
    print(f"Read model balance for ACC001: ${balance / 100:.2f}\n")

    # Publish deposit events
    deposit1 = {
        'type': 'deposit_made',
        'account_id': 'ACC001',
        'amount_cents': 25000,  # $250.00
    }
    print(f"Publishing: {deposit1}")
    publish(deposit1)

    deposit2 = {
        'type': 'deposit_made',
        'account_id': 'ACC001',
        'amount_cents': 10000,  # $100.00
    }
    print(f"Publishing: {deposit2}")
    publish(deposit2)

    # Query the updated read model
    account = read_model.get_account('ACC001')
    print(f"\nRead model account state:")
    print(f"  Balance: ${account['balance_cents'] / 100:.2f}")
    print(f"  Transactions: {account['transaction_count']}")

    # Show the audit log
    print(f"\nAudit log ({len(audit_log.get_events())} events):")
    for event in audit_log.get_events():
        print(f"  - {event['type']}")

    print("\n=== Message Bus Example Complete ===")

    # Clean up for next example
    clear()


if __name__ == "__main__":
    main()
