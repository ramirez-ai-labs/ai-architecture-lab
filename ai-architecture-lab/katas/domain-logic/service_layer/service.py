"""Service layer implementing business operations for accounts.

This module shows a simple Service Layer pattern: each method implements a unit
of business logic (create, deposit, withdraw, transfer). The Service Layer:

1. Accepts primitive types as input
2. Enforces business rules
3. Coordinates domain logic and persistence
4. Publishes events for other parts of the system

Notes for learners:
- Inputs/outputs: methods accept and return simple values (ids, amounts)
- Business rule enforcement: validates inputs and raises exceptions for violations
- No database knowledge: this layer receives a repository abstraction
- Event publishing: allows decoupled systems to react to changes
- Simplicity: focus on clarity for learning, not production optimization

This is extracted from a larger CQRS pattern but simplified for learning.
"""

from typing import Optional, Callable, List, Dict, Any
from dataclasses import dataclass


# Exception for domain business rule violations
class InsufficientFunds(Exception):
    """Raised when an operation would result in negative balance."""
    pass


@dataclass
class Account:
    """Represents an account in the system."""
    id: int
    owner: str
    balance: float


class AccountService:
    """
    Service layer for account operations.
    
    This class coordinates:
    - Business rule validation
    - Repository operations (read/write)
    - Event publishing (for decoupled subscribers)
    """
    
    def __init__(
        self,
        repository: "AccountRepository",
        event_publisher: Optional[Callable[[Dict[str, Any]], None]] = None
    ):
        """
        Initialize the service with dependencies.
        
        Args:
            repository: Handles persistence (create, read, update)
            event_publisher: Optional callback to publish events for subscribers
        """
        self.repository = repository
        self.event_publisher = event_publisher or self._noop_publisher
        self._events: List[Dict[str, Any]] = []  # In-memory event log
    
    @staticmethod
    def _noop_publisher(event: Dict[str, Any]) -> None:
        """Default no-op publisher when none is provided."""
        pass
    
    def create_account(self, owner: str, initial_balance: float = 0.0) -> int:
        """
        Create a new account.
        
        Args:
            owner: Account owner's name
            initial_balance: Starting balance (default 0.0)
        
        Returns:
            ID of the newly created account
        
        Raises:
            ValueError: If initial_balance is negative
        """
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        
        # Persist the account
        account_id = self.repository.create_account(owner, float(initial_balance))
        
        # Publish event for subscribers
        event = {
            "type": "account_created",
            "account_id": account_id,
            "owner": owner,
            "balance": float(initial_balance)
        }
        self._events.append(event)
        self.event_publisher(event)
        
        return account_id
    
    def deposit(self, account_id: int, amount: float) -> float:
        """
        Deposit money into an account.
        
        Args:
            account_id: ID of the account
            amount: Amount to deposit (must be positive)
        
        Returns:
            New balance after deposit
        
        Raises:
            ValueError: If amount is not positive
            KeyError: If account doesn't exist
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        # Get current account
        account = self.repository.get_account(account_id)
        if not account:
            raise KeyError(f"Account {account_id} not found")
        
        # Calculate new balance
        new_balance = account.balance + float(amount)
        
        # Persist the change
        self.repository.update_balance(account_id, new_balance)
        
        # Publish event
        event = {
            "type": "account_deposit",
            "account_id": account_id,
            "amount": float(amount),
            "new_balance": new_balance
        }
        self._events.append(event)
        self.event_publisher(event)
        
        return new_balance
    
    def withdraw(self, account_id: int, amount: float) -> float:
        """
        Withdraw money from an account.
        
        Args:
            account_id: ID of the account
            amount: Amount to withdraw (must be positive)
        
        Returns:
            New balance after withdrawal
        
        Raises:
            ValueError: If amount is not positive
            KeyError: If account doesn't exist
            InsufficientFunds: If withdrawal would result in negative balance
        """
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        
        # Get current account
        account = self.repository.get_account(account_id)
        if not account:
            raise KeyError(f"Account {account_id} not found")
        
        # Check business rule: sufficient funds
        if account.balance < amount:
            raise InsufficientFunds(
                f"Cannot withdraw {amount}: only {account.balance} available"
            )
        
        # Calculate new balance
        new_balance = account.balance - float(amount)
        
        # Persist the change
        self.repository.update_balance(account_id, new_balance)
        
        # Publish event
        event = {
            "type": "account_withdrawal",
            "account_id": account_id,
            "amount": float(amount),
            "new_balance": new_balance
        }
        self._events.append(event)
        self.event_publisher(event)
        
        return new_balance
    
    def transfer(
        self,
        from_account_id: int,
        to_account_id: int,
        amount: float
    ) -> None:
        """
        Transfer money between two accounts (atomic operation).
        
        Args:
            from_account_id: ID of account to transfer from
            to_account_id: ID of account to transfer to
            amount: Amount to transfer (must be positive)
        
        Raises:
            ValueError: If amount is not positive
            KeyError: If either account doesn't exist
            InsufficientFunds: If from_account has insufficient funds
        """
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        
        # Get both accounts
        from_account = self.repository.get_account(from_account_id)
        to_account = self.repository.get_account(to_account_id)
        
        if not from_account:
            raise KeyError(f"From account {from_account_id} not found")
        if not to_account:
            raise KeyError(f"To account {to_account_id} not found")
        
        # Check business rule: sufficient funds
        if from_account.balance < amount:
            raise InsufficientFunds(
                f"Cannot transfer {amount}: only {from_account.balance} available"
            )
        
        # Calculate new balances
        new_from_balance = from_account.balance - float(amount)
        new_to_balance = to_account.balance + float(amount)
        
        # Persist both changes (ideally in a transaction)
        self.repository.update_balance(from_account_id, new_from_balance)
        self.repository.update_balance(to_account_id, new_to_balance)
        
        # Publish events for both accounts
        event_from = {
            "type": "account_transfer_out",
            "from_account_id": from_account_id,
            "to_account_id": to_account_id,
            "amount": float(amount),
            "new_balance": new_from_balance
        }
        event_to = {
            "type": "account_transfer_in",
            "from_account_id": from_account_id,
            "to_account_id": to_account_id,
            "amount": float(amount),
            "new_balance": new_to_balance
        }
        
        self._events.append(event_from)
        self._events.append(event_to)
        self.event_publisher(event_from)
        self.event_publisher(event_to)
    
    def get_balance(self, account_id: int) -> float:
        """
        Get the current balance of an account.
        
        Args:
            account_id: ID of the account
        
        Returns:
            Current balance
        
        Raises:
            KeyError: If account doesn't exist
        """
        account = self.repository.get_account(account_id)
        if not account:
            raise KeyError(f"Account {account_id} not found")
        
        return account.balance
    
    def get_events(self) -> List[Dict[str, Any]]:
        """Get all events published by this service (for testing)."""
        return self._events.copy()
    
    def clear_events(self) -> None:
        """Clear the event log (useful for testing between operations)."""
        self._events.clear()


# Repository abstraction for dependency injection
class AccountRepository:
    """
    Interface for account persistence operations.
    
    In production, this would be implemented with a real database.
    In tests, we use a mock or in-memory implementation.
    """
    
    def create_account(self, owner: str, initial_balance: float) -> int:
        """Create an account and return its ID."""
        raise NotImplementedError
    
    def get_account(self, account_id: int) -> Optional[Account]:
        """Get an account by ID, or None if not found."""
        raise NotImplementedError
    
    def update_balance(self, account_id: int, new_balance: float) -> None:
        """Update an account's balance."""
        raise NotImplementedError
