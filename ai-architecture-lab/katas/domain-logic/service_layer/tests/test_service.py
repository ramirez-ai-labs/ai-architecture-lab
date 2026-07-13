"""
Unit tests for Service Layer Kata

These tests demonstrate how to test business logic with mocked dependencies,
no database required.
"""

import pytest
from unittest.mock import Mock
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from service import AccountService, AccountRepository, Account, InsufficientFunds


# Test fixture: In-memory mock repository for testing
class MockAccountRepository(AccountRepository):
    """Simple in-memory repository for testing."""
    
    def __init__(self):
        self.accounts = {}  # id -> Account
        self.next_id = 1
    
    def create_account(self, owner: str, initial_balance: float) -> int:
        acc_id = self.next_id
        self.accounts[acc_id] = Account(
            id=acc_id,
            owner=owner,
            balance=float(initial_balance)
        )
        self.next_id += 1
        return acc_id
    
    def get_account(self, account_id: int):
        return self.accounts.get(account_id)
    
    def update_balance(self, account_id: int, new_balance: float) -> None:
        if account_id in self.accounts:
            self.accounts[account_id].balance = float(new_balance)


class TestAccountServiceCreateAccount:
    """Test account creation."""
    
    def test_create_account_with_zero_balance(self):
        """Test creating an account with default zero balance."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        account_id = service.create_account("Alice")
        
        assert account_id == 1
        assert repo.get_account(account_id).owner == "Alice"
        assert repo.get_account(account_id).balance == 0.0
    
    def test_create_account_with_initial_balance(self):
        """Test creating an account with initial balance."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        account_id = service.create_account("Bob", 1000.0)
        
        assert account_id == 1
        assert repo.get_account(account_id).balance == 1000.0
    
    def test_create_account_negative_balance_raises_error(self):
        """Test that negative initial balance raises error."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        with pytest.raises(ValueError, match="Initial balance cannot be negative"):
            service.create_account("Charlie", -100.0)
    
    def test_create_account_publishes_event(self):
        """Test that account creation publishes an event."""
        repo = MockAccountRepository()
        publisher = Mock()
        service = AccountService(repo, event_publisher=publisher)
        
        account_id = service.create_account("Diana", 500.0)
        
        # Verify event was published
        publisher.assert_called_once()
        event = publisher.call_args[0][0]
        assert event["type"] == "account_created"
        assert event["account_id"] == account_id
        assert event["owner"] == "Diana"
        assert event["balance"] == 500.0


class TestAccountServiceDeposit:
    """Test deposit operations."""
    
    def test_deposit_positive_amount(self):
        """Test depositing money into an account."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        acc_id = service.create_account("Alice", 100.0)
        service.clear_events()  # Reset events
        
        new_balance = service.deposit(acc_id, 50.0)
        
        assert new_balance == 150.0
        assert repo.get_account(acc_id).balance == 150.0
    
    def test_deposit_zero_amount_raises_error(self):
        """Test that depositing zero raises error."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        acc_id = service.create_account("Bob", 100.0)
        
        with pytest.raises(ValueError, match="Deposit amount must be positive"):
            service.deposit(acc_id, 0)
    
    def test_deposit_negative_amount_raises_error(self):
        """Test that depositing negative amount raises error."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        acc_id = service.create_account("Charlie", 100.0)
        
        with pytest.raises(ValueError, match="Deposit amount must be positive"):
            service.deposit(acc_id, -50.0)
    
    def test_deposit_nonexistent_account_raises_error(self):
        """Test that depositing to nonexistent account raises error."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        with pytest.raises(KeyError, match="Account 999 not found"):
            service.deposit(999, 50.0)
    
    def test_deposit_publishes_event(self):
        """Test that deposit publishes an event."""
        repo = MockAccountRepository()
        publisher = Mock()
        service = AccountService(repo, event_publisher=publisher)
        
        acc_id = service.create_account("Diana", 100.0)
        publisher.reset_mock()  # Clear creation event
        
        service.deposit(acc_id, 75.0)
        
        # Verify event was published
        publisher.assert_called_once()
        event = publisher.call_args[0][0]
        assert event["type"] == "account_deposit"
        assert event["account_id"] == acc_id
        assert event["amount"] == 75.0
        assert event["new_balance"] == 175.0


class TestAccountServiceWithdraw:
    """Test withdrawal operations."""
    
    def test_withdraw_from_sufficient_balance(self):
        """Test withdrawing when sufficient funds exist."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        acc_id = service.create_account("Frank", 500.0)
        
        new_balance = service.withdraw(acc_id, 200.0)
        
        assert new_balance == 300.0
        assert repo.get_account(acc_id).balance == 300.0
    
    def test_withdraw_insufficient_funds_raises_error(self):
        """Test that withdrawal with insufficient funds raises error."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        acc_id = service.create_account("Grace", 100.0)
        
        with pytest.raises(InsufficientFunds):
            service.withdraw(acc_id, 150.0)
    
    def test_withdraw_exact_balance(self):
        """Test withdrawing exact balance (edge case)."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        acc_id = service.create_account("Helen", 500.0)
        
        new_balance = service.withdraw(acc_id, 500.0)
        
        assert new_balance == 0.0
    
    def test_withdraw_zero_amount_raises_error(self):
        """Test that withdrawing zero raises error."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        acc_id = service.create_account("Ivy", 500.0)
        
        with pytest.raises(ValueError, match="Withdraw amount must be positive"):
            service.withdraw(acc_id, 0)
    
    def test_withdraw_negative_amount_raises_error(self):
        """Test that withdrawing negative raises error."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        acc_id = service.create_account("Jack", 500.0)
        
        with pytest.raises(ValueError, match="Withdraw amount must be positive"):
            service.withdraw(acc_id, -100.0)
    
    def test_withdraw_nonexistent_account_raises_error(self):
        """Test that withdrawing from nonexistent account raises error."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        with pytest.raises(KeyError, match="Account 999 not found"):
            service.withdraw(999, 50.0)
    
    def test_withdraw_publishes_event(self):
        """Test that withdrawal publishes an event."""
        repo = MockAccountRepository()
        publisher = Mock()
        service = AccountService(repo, event_publisher=publisher)
        
        acc_id = service.create_account("Kate", 500.0)
        publisher.reset_mock()
        
        service.withdraw(acc_id, 100.0)
        
        # Verify event was published
        publisher.assert_called_once()
        event = publisher.call_args[0][0]
        assert event["type"] == "account_withdrawal"
        assert event["account_id"] == acc_id
        assert event["amount"] == 100.0
        assert event["new_balance"] == 400.0


class TestAccountServiceTransfer:
    """Test transfer operations."""
    
    def test_transfer_between_accounts(self):
        """Test transferring money between accounts."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        from_id = service.create_account("Liam", 1000.0)
        to_id = service.create_account("Mina", 500.0)
        
        service.clear_events()
        service.transfer(from_id, to_id, 200.0)
        
        assert repo.get_account(from_id).balance == 800.0
        assert repo.get_account(to_id).balance == 700.0
    
    def test_transfer_insufficient_funds_raises_error(self):
        """Test that transfer with insufficient funds raises error."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        from_id = service.create_account("Noah", 100.0)
        to_id = service.create_account("Olivia", 500.0)
        
        with pytest.raises(InsufficientFunds):
            service.transfer(from_id, to_id, 150.0)
    
    def test_transfer_to_nonexistent_account_raises_error(self):
        """Test transfer to nonexistent account raises error."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        from_id = service.create_account("Paul", 1000.0)
        
        with pytest.raises(KeyError, match="To account 999 not found"):
            service.transfer(from_id, 999, 100.0)
    
    def test_transfer_from_nonexistent_account_raises_error(self):
        """Test transfer from nonexistent account raises error."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        to_id = service.create_account("Quinn", 500.0)
        
        with pytest.raises(KeyError, match="From account 999 not found"):
            service.transfer(999, to_id, 100.0)
    
    def test_transfer_zero_amount_raises_error(self):
        """Test that transferring zero raises error."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        from_id = service.create_account("Rachel", 1000.0)
        to_id = service.create_account("Sam", 500.0)
        
        with pytest.raises(ValueError, match="Transfer amount must be positive"):
            service.transfer(from_id, to_id, 0)
    
    def test_transfer_negative_amount_raises_error(self):
        """Test that transferring negative raises error."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        from_id = service.create_account("Tara", 1000.0)
        to_id = service.create_account("Uma", 500.0)
        
        with pytest.raises(ValueError, match="Transfer amount must be positive"):
            service.transfer(from_id, to_id, -100.0)
    
    def test_transfer_publishes_two_events(self):
        """Test that transfer publishes events for both accounts."""
        repo = MockAccountRepository()
        publisher = Mock()
        service = AccountService(repo, event_publisher=publisher)
        
        from_id = service.create_account("Victor", 1000.0)
        to_id = service.create_account("Wendy", 500.0)
        
        publisher.reset_mock()
        service.transfer(from_id, to_id, 250.0)
        
        # Should be called twice (once for each account)
        assert publisher.call_count == 2


class TestAccountServiceGetBalance:
    """Test balance queries."""
    
    def test_get_balance_existing_account(self):
        """Test getting balance of existing account."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        acc_id = service.create_account("Zane", 750.0)
        
        balance = service.get_balance(acc_id)
        
        assert balance == 750.0
    
    def test_get_balance_nonexistent_account_raises_error(self):
        """Test that getting balance of nonexistent account raises error."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        with pytest.raises(KeyError, match="Account 999 not found"):
            service.get_balance(999)


class TestIntegrationScenarios:
    """Integration tests for realistic workflows."""
    
    def test_full_account_lifecycle(self):
        """Test complete account workflow."""
        repo = MockAccountRepository()
        publisher = Mock()
        service = AccountService(repo, event_publisher=publisher)
        
        # Create account
        acc_id = service.create_account("Integration", 1000.0)
        
        # Perform operations
        service.deposit(acc_id, 500.0)
        service.withdraw(acc_id, 200.0)
        
        # Verify final state
        assert service.get_balance(acc_id) == 1300.0
        
        # Verify events were published
        assert publisher.call_count == 3
    
    def test_multiple_account_transfers(self):
        """Test multiple transfers between accounts."""
        repo = MockAccountRepository()
        service = AccountService(repo)
        
        # Create three accounts
        alice_id = service.create_account("Alice", 1000.0)
        bob_id = service.create_account("Bob", 500.0)
        charlie_id = service.create_account("Charlie", 750.0)
        
        service.clear_events()
        
        # Alice transfers to Bob
        service.transfer(alice_id, bob_id, 200.0)
        
        # Bob transfers to Charlie
        service.transfer(bob_id, charlie_id, 150.0)
        
        # Verify final balances
        assert service.get_balance(alice_id) == 800.0
        assert service.get_balance(bob_id) == 550.0
        assert service.get_balance(charlie_id) == 900.0
