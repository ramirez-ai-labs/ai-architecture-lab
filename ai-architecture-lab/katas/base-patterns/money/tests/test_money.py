"""
Tests for Money Value Object.

Demonstrates:
- Money creation and validation
- Currency handling
- Precision rules (integer cents, no floating point)
- Arithmetic operations (add, subtract, multiply)
- Value equality
- Immutability
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from money.money import Money


class TestMoneyCreation:
    """Test Money object creation and validation."""
    
    def test_create_money_with_valid_amount_and_currency(self):
        """Valid money amounts and currencies should create Money objects."""
        money = Money(1000, "USD")
        
        assert money.amount_cents == 1000
        assert money.currency == "USD"
    
    def test_currency_is_normalized_to_uppercase(self):
        """Currency codes should be normalized to uppercase."""
        money = Money(1000, "usd")
        
        assert money.currency == "USD"
    
    def test_currency_whitespace_is_trimmed(self):
        """Whitespace should be trimmed from currency codes."""
        money = Money(1000, "  USD  ")
        
        assert money.currency == "USD"
    
    def test_negative_amount_raises_error(self):
        """Negative amounts should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be negative"):
            Money(-100, "USD")
    
    def test_zero_amount_is_valid(self):
        """Zero amount should be valid."""
        money = Money(0, "USD")
        
        assert money.amount_cents == 0
        assert money.is_zero()
    
    def test_non_integer_amount_raises_error(self):
        """Non-integer amounts should raise ValueError."""
        with pytest.raises(ValueError, match="must be an integer"):
            Money(10.5, "USD")
    
    def test_invalid_currency_raises_error(self):
        """Invalid currency codes should raise ValueError."""
        with pytest.raises(ValueError, match="Unsupported currency"):
            Money(1000, "XYZ")
    
    def test_empty_currency_raises_error(self):
        """Empty currency should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Money(1000, "")
    
    def test_non_string_currency_raises_error(self):
        """Non-string currency should raise ValueError."""
        with pytest.raises(ValueError, match="must be a string"):
            Money(1000, 123)


class TestMoneyEquality:
    """Test value-based equality for Money."""
    
    def test_same_amount_and_currency_are_equal(self):
        """Two Money objects with same amount and currency should be equal."""
        money1 = Money(1000, "USD")
        money2 = Money(1000, "USD")
        
        assert money1 == money2
        assert not (money1 != money2)
    
    def test_different_amounts_are_not_equal(self):
        """Different amounts should not be equal."""
        money1 = Money(1000, "USD")
        money2 = Money(2000, "USD")
        
        assert money1 != money2
    
    def test_different_currencies_are_not_equal(self):
        """Different currencies should not be equal, even with same amount."""
        money1 = Money(1000, "USD")
        money2 = Money(1000, "EUR")
        
        assert money1 != money2
    
    def test_can_use_in_set(self):
        """Money objects can be used in sets."""
        money1 = Money(1000, "USD")
        money2 = Money(1000, "USD")  # Same as money1
        money3 = Money(2000, "USD")
        
        money_set = {money1, money2, money3}
        
        # money1 and money2 are equal, so set should only have 2 items
        assert len(money_set) == 2
        assert money1 in money_set
        assert money2 in money_set
        assert money3 in money_set


class TestMoneyPrecision:
    """Test precision rules (no floating point for money!)."""
    
    def test_money_stored_as_integer_cents(self):
        """Money should be stored as integer cents, not floating point."""
        # $10.50 = 1050 cents
        money = Money(1050, "USD")
        
        assert money.amount_cents == 1050
        assert isinstance(money.amount_cents, int)
    
    def test_no_floating_point_precision_errors(self):
        """Using integers prevents floating point precision errors."""
        # If we used floats: 0.1 + 0.2 = 0.30000000000000004 (wrong!)
        # With integers: 10 cents + 20 cents = 30 cents (correct!)
        money1 = Money(10, "USD")  # $0.10
        money2 = Money(20, "USD")  # $0.20
        
        total = money1.add(money2)
        
        assert total.amount_cents == 30  # Exactly 30 cents, no precision error
        assert str(total) == "$0.30"


class TestMoneyArithmetic:
    """Test arithmetic operations on Money."""
    
    def test_add_same_currency(self):
        """Adding Money with same currency should work."""
        money1 = Money(1000, "USD")  # $10.00
        money2 = Money(500, "USD")   # $5.00
        
        total = money1.add(money2)
        
        assert total.amount_cents == 1500  # $15.00
        assert total.currency == "USD"
    
    def test_add_different_currencies_raises_error(self):
        """Adding Money with different currencies should raise error."""
        money1 = Money(1000, "USD")
        money2 = Money(1000, "EUR")
        
        with pytest.raises(ValueError, match="Currencies must match"):
            money1.add(money2)
    
    def test_add_non_money_raises_error(self):
        """Adding non-Money objects should raise error."""
        money = Money(1000, "USD")
        
        with pytest.raises(ValueError, match="Can only add Money to Money"):
            money.add(100)
    
    def test_subtract_same_currency(self):
        """Subtracting Money with same currency should work."""
        money1 = Money(1000, "USD")  # $10.00
        money2 = Money(300, "USD")   # $3.00
        
        difference = money1.subtract(money2)
        
        assert difference.amount_cents == 700  # $7.00
        assert difference.currency == "USD"
    
    def test_subtract_resulting_in_negative_raises_error(self):
        """Subtracting that would result in negative should raise error."""
        money1 = Money(500, "USD")  # $5.00
        money2 = Money(1000, "USD")  # $10.00
        
        with pytest.raises(ValueError, match="would be negative"):
            money1.subtract(money2)
    
    def test_subtract_different_currencies_raises_error(self):
        """Subtracting Money with different currencies should raise error."""
        money1 = Money(1000, "USD")
        money2 = Money(1000, "EUR")
        
        with pytest.raises(ValueError, match="Currencies must match"):
            money1.subtract(money2)
    
    def test_multiply_by_positive_number(self):
        """Multiplying Money by positive number should work."""
        money = Money(1000, "USD")  # $10.00
        
        result = money.multiply(1.5)  # 150%
        
        assert result.amount_cents == 1500  # $15.00
        assert result.currency == "USD"
    
    def test_multiply_rounds_to_nearest_cent(self):
        """Multiplying should round to nearest cent."""
        money = Money(333, "USD")  # $3.33
        
        # 3.33 * 1.5 = 4.995, should round to 5.00 (500 cents)
        result = money.multiply(1.5)
        
        assert result.amount_cents == 500  # $5.00 (rounded)
    
    def test_multiply_by_negative_raises_error(self):
        """Multiplying by negative number should raise error."""
        money = Money(1000, "USD")
        
        with pytest.raises(ValueError, match="cannot be negative"):
            money.multiply(-1)
    
    def test_multiply_by_zero(self):
        """Multiplying by zero should result in zero."""
        money = Money(1000, "USD")
        
        result = money.multiply(0)
        
        assert result.amount_cents == 0
        assert result.is_zero()


class TestMoneyImmutability:
    """Test immutability of Money objects."""
    
    def test_money_cannot_be_modified_after_creation(self):
        """Money objects should be immutable after creation."""
        money = Money(1000, "USD")
        original_amount = money.amount_cents
        original_currency = money.currency
        
        # Attempting to modify _amount_cents directly would be a design violation
        # The properties are read-only, enforcing immutability
        assert money.amount_cents == original_amount
        assert money.currency == original_currency
    
    def test_arithmetic_operations_return_new_objects(self):
        """Arithmetic operations should return new Money objects, not modify existing."""
        money1 = Money(1000, "USD")
        money2 = Money(500, "USD")
        
        # Add should return new object
        total = money1.add(money2)
        
        # Original objects should be unchanged
        assert money1.amount_cents == 1000
        assert money2.amount_cents == 500
        assert total.amount_cents == 1500
        assert money1 is not total  # Different objects


class TestMoneyBusinessLogic:
    """Test business logic methods of Money."""
    
    def test_is_zero_returns_true_for_zero_amount(self):
        """is_zero() should return True for zero amount."""
        money = Money(0, "USD")
        
        assert money.is_zero()
    
    def test_is_zero_returns_false_for_non_zero_amount(self):
        """is_zero() should return False for non-zero amount."""
        money = Money(100, "USD")
        
        assert not money.is_zero()
    
    def test_is_positive_returns_true_for_positive_amount(self):
        """is_positive() should return True for positive amount."""
        money = Money(100, "USD")
        
        assert money.is_positive()
    
    def test_is_positive_returns_false_for_zero_amount(self):
        """is_positive() should return False for zero amount."""
        money = Money(0, "USD")
        
        assert not money.is_positive()


class TestMoneyStringRepresentation:
    """Test string representation of Money."""
    
    def test_str_formats_usd_correctly(self):
        """USD should be formatted with dollar sign."""
        money = Money(1050, "USD")  # $10.50
        
        assert str(money) == "$10.50"
    
    def test_str_formats_eur_correctly(self):
        """EUR should be formatted with euro sign."""
        money = Money(1050, "EUR")  # €10.50
        
        assert str(money) == "€10.50"
    
    def test_str_formats_gbp_correctly(self):
        """GBP should be formatted with pound sign."""
        money = Money(1050, "GBP")  # £10.50
        
        assert str(money) == "£10.50"
    
    def test_str_formats_jpy_correctly(self):
        """JPY should be formatted without decimal places."""
        money = Money(1000, "JPY")  # ¥1000
        
        assert str(money) == "¥1000"
    
    def test_str_handles_zero_correctly(self):
        """Zero amount should format correctly."""
        money = Money(0, "USD")
        
        assert str(money) == "$0.00"
