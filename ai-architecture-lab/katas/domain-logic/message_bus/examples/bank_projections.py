"""Example: Bank account events coordinated by a message bus.

SCENARIO:
We're building a banking system. When a user creates an account or deposits money,
the system needs to:
- Update the account balance (read model for queries)
- Log the event for audit/compliance
- Send a confirmation notification (skipped in this example for simplicity)

PROBLEM WITHOUT MESSAGE BUS (tightly coupled):
    account_service.create_account()
        -> Update read model (direct call)
        -> Log to audit (direct call)
        -> Send notification (direct call)

This couples the business logic to infrastructure, making tests hard and changes risky.

SOLUTION WITH MESSAGE BUS (decoupled):
    account_service.create_account()
    -> publish({'type': 'account_created', 'account_id': 'ACC001'})
    -> Read model listens and updates independently
    -> Audit log listens and records independently
    -> Notification service listens and sends independently

This is the CQRS (Command Query Responsibility Segregation) pattern:
- WRITE SIDE: Account creation publishes events
- READ SIDE: Multiple projections listen and build their own views

THIS EXAMPLE DEMONSTRATES:
1. Two independent projections (read model + audit log) listening to events
2. Domain events (AccountCreated, DepositMade) as the contract between components
3. How changing the read model doesn't affect the write side
4. How adding new projections (handlers) doesn't require changing existing code
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from message_bus import subscribe, publish, clear


class AccountReadModel:
    """A read-model projection that listens to account events.

    WHAT IS A READ MODEL PROJECTION?
    A read-model projection is a separate data store optimized for querying.
    It listens to domain events and updates itself based on what happened.

    IN THIS EXAMPLE:
    AccountReadModel maintains an in-memory cache of account balances and metadata.
    When AccountCreated event occurs, it creates a new account entry.
    When DepositMade event occurs, it updates the balance.

    KEY DESIGN PRINCIPLES:
    1. EVENTUAL CONSISTENCY: The read model is updated AFTER the event is published
    2. INDEPENDENT: The read model doesn't affect the write side
    3. EASY TO CHANGE: You can modify the read model without touching business logic
    4. EASY TO TEST: Subscribe to events and verify the read model updates

    WHY SEPARATE READ AND WRITE?
    - Write side (creating an account): Complex business logic, consistency checks
    - Read side (querying balances): Fast, simple, optimized for queries
    - Separating them lets each evolve independently
    """

    def __init__(self):
        """Initialize the read model with an empty account cache."""
        # Store accounts as a dict: account_id -> account_state
        # account_state includes: balance_cents (integer), transaction_count (number of operations)
        self.accounts = {}

    def on_account_created(self, event):
        """Handle AccountCreated event by creating a new account entry.

        WHAT HAPPENS:
        1. Check if this is an account_created event (ignore other events)
        2. Extract the account_id and initial balance from the event
        3. Create a new entry in our read model

        WHY CHECK THE EVENT TYPE?
        We subscribe to ALL events, so we see AccountCreated, DepositMade, etc.
        We only care about AccountCreated, so we check the type and return early
        if it's not the event we want.
        """
        # Only handle account_created events (ignore all others)
        if event['type'] != 'account_created':
            return

        # Extract the account ID from the event
        account_id = event['account_id']

        # Extract the initial balance from the event, default to 0 if not provided
        initial_balance = event.get('initial_balance_cents', 0)

        # Create a new account entry in our read model cache
        # Store balance and transaction count (how many operations)
        self.accounts[account_id] = {
            'balance_cents': initial_balance,
            'transaction_count': 0,
        }

    def on_deposit_made(self, event):
        """Handle DepositMade event by updating the account balance.

        WHAT HAPPENS:
        1. Check if this is a deposit_made event (ignore other events)
        2. Extract the account_id and deposit amount from the event
        3. Find the account in our read model
        4. Increase the balance and transaction count
        """
        # Only handle deposit_made events (ignore all others)
        if event['type'] != 'deposit_made':
            return

        # Extract the account ID and deposit amount from the event
        account_id = event['account_id']
        deposit_amount = event['amount_cents']

        # Find the account in our read model and update it
        if account_id in self.accounts:
            # Add the deposit to the account balance
            self.accounts[account_id]['balance_cents'] += deposit_amount
            # Increment the transaction counter
            self.accounts[account_id]['transaction_count'] += 1

    def get_balance(self, account_id):
        """Query the read model for an account's balance.

        Returns the balance in cents, or None if account not found.
        This is a read-only query against our read model cache.
        """
        # Check if account exists in our read model
        if account_id not in self.accounts:
            return None

        # Return the balance from our cached account state
        return self.accounts[account_id]['balance_cents']

    def get_account(self, account_id):
        """Query the read model for full account information.

        Returns the entire account dict (balance, transaction_count, etc)
        or None if account not found.
        """
        # Return the full account dict from our read model cache
        return self.accounts.get(account_id)


class AuditLog:
    """An audit log that records all events for compliance and traceability.

    WHAT IS AN AUDIT LOG PROJECTION?
    An audit log is another type of read model that records EVERYTHING for:
    - Compliance: Prove what happened and when (regulatory requirements)
    - Debugging: Understand the full history of changes
    - Forensics: Investigate issues after they occur
    - Analytics: See patterns in what users do

    KEY DIFFERENCE FROM AccountReadModel:
    - AccountReadModel: Stores the CURRENT state (balance, etc)
    - AuditLog: Stores the COMPLETE HISTORY (every event ever)

    WHY BOTH EXIST IN A MESSAGE BUS SYSTEM:
    Multiple projections listening to the same events:
    - One optimized for queries (AccountReadModel)
    - One optimized for compliance (AuditLog)
    - More could exist: notification log, analytics pipeline, etc.
    """

    def __init__(self):
        """Initialize the audit log with an empty event list."""
        # Store all events in order they occurred
        self.events = []

    def record(self, event):
        """Record an event in the audit log.

        This handler is called for EVERY event published.
        We append it to our log for historical record.

        NOTE: This handler ignores event type - it records everything.
        Compared to AccountReadModel which filters by type.
        """
        # Simply append the event to our historical record
        self.events.append(event)

    def get_events(self):
        """Retrieve all recorded events as a list.

        Returns a copy of the events list (defensive copy).
        Caller can iterate through the full event history.
        """
        # Return a copy so external modifications don't affect our log
        return list(self.events)


def main():
    """Run the bank account message bus example.

    FLOW OF THIS EXAMPLE:
    1. Create two projections (read model + audit log)
    2. Subscribe them to the message bus
    3. Publish domain events (account creation + deposits)
    4. Show how each projection reacted to the events
    5. Clean up the message bus for the next example
    """
    print("=== Bank Account with Message Bus ===\n")

    # STEP 1: Create projections.
    # Each projection will listen to events and maintain its own state.
    read_model = AccountReadModel()      # Tracks current account state
    audit_log = AuditLog()               # Records full history

    # STEP 2: Subscribe projections to the message bus.
    # When events are published, each projection's handlers will be called.
    #
    # AccountReadModel has two handlers:
    subscribe(read_model.on_account_created)  # Handles account_created events
    subscribe(read_model.on_deposit_made)     # Handles deposit_made events
    #
    # AuditLog has one handler that records everything:
    subscribe(audit_log.record)               # Records all events

    print("--- Publishing domain events ---\n")

    # STEP 3: Publish an account creation event.
    # This is what the write-side (account creation logic) does.
    # It doesn't call the read models directly - it publishes an event.
    #
    # Event structure:
    # - 'type': the event type (account_created, deposit_made, etc)
    # - Additional fields: domain data (account_id, amount_cents, etc)
    create_event = {
        'type': 'account_created',
        'account_id': 'ACC001',
        'initial_balance_cents': 50000,  # Initial balance: $500.00
    }
    print(f"Publishing: {create_event}")
    publish(create_event)
    # When publish() is called:
    # 1. read_model.on_account_created() is called -> creates account entry
    # 2. read_model.on_deposit_made() is called -> ignores (not a deposit)
    # 3. audit_log.record() is called -> logs the event

    # STEP 4: Query the read model to verify it was updated.
    # The read model now has the account we just created.
    balance = read_model.get_balance('ACC001')
    print(f"Read model balance for ACC001: ${balance / 100:.2f}\n")
    # Output shows $500.00 (the initial balance)

    # STEP 5: Publish multiple deposit events.
    # We'll add two deposits and see the read model update each time.

    # First deposit: $250.00
    deposit1 = {
        'type': 'deposit_made',
        'account_id': 'ACC001',
        'amount_cents': 25000,  # $250.00
    }
    print(f"Publishing: {deposit1}")
    publish(deposit1)
    # read_model.on_deposit_made() updates the balance and transaction count

    # Second deposit: $100.00
    deposit2 = {
        'type': 'deposit_made',
        'account_id': 'ACC001',
        'amount_cents': 10000,  # $100.00
    }
    print(f"Publishing: {deposit2}")
    publish(deposit2)
    # read_model.on_deposit_made() updates the balance and transaction count

    # STEP 6: Query the read model to see the final state.
    # The read model now reflects both deposits.
    account = read_model.get_account('ACC001')
    print(f"\nRead model account state:")
    # Calculate and display the final balance
    final_balance = account['balance_cents'] / 100
    print(f"  Balance: ${final_balance:.2f}")
    # Output: $850.00 (500 + 250 + 100)
    print(f"  Transactions: {account['transaction_count']}")
    # Output: 2 (the two deposits)

    # STEP 7: Show the audit log.
    # The audit log has recorded ALL events (not just deposits).
    audit_events = audit_log.get_events()
    print(f"\nAudit log ({len(audit_events)} events):")
    for event in audit_events:
        print(f"  - {event['type']}")
    # Output:
    # - account_created
    # - deposit_made
    # - deposit_made

    print("\n=== Message Bus Example Complete ===")

    # STEP 8: Clean up the message bus for the next example.
    # Clear all subscribers so they don't affect other examples.
    # This is important for testing - each test should start clean.
    clear()


if __name__ == "__main__":
    main()
