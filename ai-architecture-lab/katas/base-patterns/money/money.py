"""
Money Value Object Pattern

A specialized Value Object for representing monetary amounts with currency.

Key characteristics:
- Immutable: Once created, cannot be modified
- Precision-safe: Uses integer cents/pennies (no floating point!)
- Currency-aware: Tracks currency code (USD, EUR, etc.)
- Arithmetic operations: add, subtract, multiply
- Value equality: Two Money objects with same amount and currency are equal

Why use integers for money?
- Floating point arithmetic has precision errors
- Example: 0.1 + 0.2 = 0.30000000000000004 (wrong!)
- Solution: Store cents as integers (100 cents = $1.00)
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from value_object import ValueObject


class Money(ValueObject):
    """
    Money value object representing a monetary amount with currency.
    
    Characteristics:
    - Immutable: Once created, cannot be modified
    - Precision-safe: Stores amount as integer cents (no floating point)
    - Currency-aware: Tracks currency code (USD, EUR, GBP, etc.)
    - Arithmetic operations: add, subtract, multiply
    - Value equality: Two Money objects with same amount and currency are equal
    
    Example:
        >>> money1 = Money(1000, "USD")  # $10.00
        >>> money2 = Money(500, "USD")   # $5.00
        >>> total = money1.add(money2)   # $15.00
        >>> print(total)
        $15.00
    """
    
    # Supported currency codes (ISO 4217)
    SUPPORTED_CURRENCIES = {"USD", "EUR", "GBP", "JPY", "CAD", "AUD"}
    
    def __init__(self, amount_cents: int, currency: str):
        """
        Create a Money value object.
        
        Args:
            amount_cents: Amount in smallest currency unit (cents for USD, pence for GBP)
            currency: Currency code (USD, EUR, GBP, etc.)
            
        Raises:
            ValueError: If amount_cents is negative or currency is invalid
        """
        if not isinstance(amount_cents, int):
            raise ValueError("amount_cents must be an integer")
        
        if amount_cents < 0:
            raise ValueError("Amount cannot be negative")
        
        if not isinstance(currency, str):
            raise ValueError("Currency must be a string")
        
        currency = currency.upper().strip()
        
        if not currency:
            raise ValueError("Currency cannot be empty")
        
        if currency not in self.SUPPORTED_CURRENCIES:
            raise ValueError(
                f"Unsupported currency: {currency}. "
                f"Supported: {', '.join(sorted(self.SUPPORTED_CURRENCIES))}"
            )
        
        # Store as private attributes to enforce immutability
        self._amount_cents = amount_cents
        self._currency = currency
    
    @property
    def amount_cents(self) -> int:
        """Get the amount in cents (read-only)."""
        return self._amount_cents
    
    @property
    def currency(self) -> str:
        """Get the currency code (read-only)."""
        return self._currency
    
    def _get_equality_components(self) -> tuple:
        """Money equality is based on amount and currency."""
        return (self._amount_cents, self._currency)
    
    def add(self, other: 'Money') -> 'Money':
        """
        Add another Money amount to this one.
        
        Args:
            other: Another Money object to add
            
        Returns:
            New Money object with the sum
            
        Raises:
            ValueError: If currencies don't match
        """
        if not isinstance(other, Money):
            raise ValueError("Can only add Money to Money")
        
        if self._currency != other._currency:
            raise ValueError(
                f"Cannot add {self._currency} and {other._currency}. "
                "Currencies must match."
            )
        
        total_cents = self._amount_cents + other._amount_cents
        return Money(total_cents, self._currency)
    
    def subtract(self, other: 'Money') -> 'Money':
        """
        Subtract another Money amount from this one.
        
        Args:
            other: Another Money object to subtract
            
        Returns:
            New Money object with the difference
            
        Raises:
            ValueError: If currencies don't match or result would be negative
        """
        if not isinstance(other, Money):
            raise ValueError("Can only subtract Money from Money")
        
        if self._currency != other._currency:
            raise ValueError(
                f"Cannot subtract {other._currency} from {self._currency}. "
                "Currencies must match."
            )
        
        difference_cents = self._amount_cents - other._amount_cents
        
        if difference_cents < 0:
            raise ValueError(
                f"Result would be negative: {self} - {other}"
            )
        
        return Money(difference_cents, self._currency)
    
    def multiply(self, multiplier: float) -> 'Money':
        """
        Multiply this Money amount by a multiplier.
        
        Args:
            multiplier: Multiplier (e.g., 1.5 for 150%)
            
        Returns:
            New Money object with the multiplied amount
            
        Raises:
            ValueError: If multiplier is negative
        """
        if not isinstance(multiplier, (int, float)):
            raise ValueError("Multiplier must be a number")
        
        if multiplier < 0:
            raise ValueError("Multiplier cannot be negative")
        
        # Multiply and round to nearest cent
        result_cents = round(self._amount_cents * multiplier)
        return Money(result_cents, self._currency)
    
    def is_zero(self) -> bool:
        """
        Check if this Money amount is zero.
        
        Returns:
            bool: True if amount is zero
        """
        return self._amount_cents == 0
    
    def is_positive(self) -> bool:
        """
        Check if this Money amount is positive (greater than zero).
        
        Returns:
            bool: True if amount is positive
        """
        return self._amount_cents > 0
    
    def __str__(self) -> str:
        """
        String representation of Money.
        
        Returns:
            str: Formatted money string (e.g., "$10.50" for USD)
        """
        # Convert cents to dollars
        dollars = self._amount_cents / 100.0
        
        # Format based on currency
        if self._currency == "USD":
            return f"${dollars:.2f}"
        elif self._currency == "EUR":
            return f"€{dollars:.2f}"
        elif self._currency == "GBP":
            return f"£{dollars:.2f}"
        elif self._currency == "JPY":
            # JPY doesn't use decimal places
            return f"¥{self._amount_cents}"
        else:
            return f"{dollars:.2f} {self._currency}"
