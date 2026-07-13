"""
Examples demonstrating the Service Layer Kata

This module shows practical usage of the AccountService.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from service import AccountService, AccountRepository, Account


class MockAccountRepository(AccountRepository):
    """Simple in-memory repository for examples."""
    
    def __init__(self):
        self.accounts = {}
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


def example_basic_operations():
    """Example 1: Basic account operations."""
    print("=== Example 1: Basic Account Operations ===\n")
    
    repo = MockAccountRepository()
    service = AccountService(repo)
    
    # Create accounts
    alice_id = service.create_account("Alice", 1000.0)
    bob_id = service.create_account("Bob", 500.0)
    
    print(f"Created Alice's account (ID: {alice_id}) with balance: {service.get_balance(alice_id)}")
    print(f"Created Bob's account (ID: {bob_id}) with balance: {service.get_balance(bob_id)}\n")
    
    # Deposit
    new_balance = service.deposit(alice_id, 200.0)
    print(f"Alice deposited $200. New balance: {new_balance}")
    
    # Withdraw
    new_balance = service.withdraw(alice_id, 150.0)
    print(f"Alice withdrew $150. New balance: {new_balance}\n")


def example_transfer():
    """Example 2: Transfer between accounts."""
    print("=== Example 2: Transfer Between Accounts ===\n")
    
    repo = MockAccountRepository()
    service = AccountService(repo)
    
    alice_id = service.create_account("Alice", 1000.0)
    bob_id = service.create_account("Bob", 500.0)
    
    print(f"Before transfer:")
    print(f"  Alice: ${service.get_balance(alice_id)}")
    print(f"  Bob: ${service.get_balance(bob_id)}\n")
    
    # Transfer
    service.transfer(alice_id, bob_id, 300.0)
    
    print(f"Alice transferred $300 to Bob\n")
    print(f"After transfer:")
    print(f"  Alice: ${service.get_balance(alice_id)}")
    print(f"  Bob: ${service.get_balance(bob_id)}\n")


def example_error_handling():
    """Example 3: Business rule validation."""
    print("=== Example 3: Error Handling & Business Rules ===\n")
    
    repo = MockAccountRepository()
    service = AccountService(repo)
    
    acc_id = service.create_account("Diana", 100.0)
    print(f"Created account with balance: $100\n")
    
    # Try insufficient funds
    print("Attempting to withdraw $150...\n")
    try:
        service.withdraw(acc_id, 150.0)
    except Exception as e:
        print(f"Error caught: {type(e).__name__}: {e}\n")
    
    # Try negative amount
    print("Attempting to deposit -$50...\n")
    try:
        service.deposit(acc_id, -50.0)
    except ValueError as e:
        print(f"Error caught: {type(e).__name__}: {e}\n")


if __name__ == "__main__":
    example_basic_operations()
    example_transfer()
    example_error_handling()
    print("All examples completed!")
