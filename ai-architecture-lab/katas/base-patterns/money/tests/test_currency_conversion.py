"""
Tests for Currency Conversion Example.

Demonstrates currency conversion functionality.
"""

import pytest
import sys
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from money.money import Money
from ..examples.currency_conversion import convert_currency


class TestCurrencyConversion:
    """Test currency conversion functionality."""
    
    def test_convert_usd_to_eur(self):
        """Converting USD to EUR should work."""
        usd_money = Money(1000, "USD")  # $10.00
        
        eur_money = convert_currency(usd_money, "EUR")
        
        # Should convert using exchange rate (1000 * 0.85 = 850 cents)
        assert eur_money.currency == "EUR"
        assert eur_money.amount_cents == 850  # €8.50
    
    def test_convert_eur_to_usd(self):
        """Converting EUR to USD should work."""
        eur_money = Money(1000, "EUR")  # €10.00
        
        usd_money = convert_currency(eur_money, "USD")
        
        # Should convert using exchange rate (1000 * 1.18 = 1180 cents)
        assert usd_money.currency == "USD"
        assert usd_money.amount_cents == 1180  # $11.80
    
    def test_convert_same_currency_returns_same(self):
        """Converting to same currency should return same Money."""
        money = Money(1000, "USD")
        
        result = convert_currency(money, "USD")
        
        assert result == money
        assert result.amount_cents == money.amount_cents
    
    def test_convert_to_jpy_handles_no_decimal_places(self):
        """Converting to JPY should handle no decimal places correctly."""
        usd_money = Money(1000, "USD")  # $10.00
        
        jpy_money = convert_currency(usd_money, "JPY")
        
        # JPY doesn't use decimal places, so conversion is different
        assert jpy_money.currency == "JPY"
        # 1000 cents * 110.0 / 100 = 1100 JPY
        assert jpy_money.amount_cents == 1100
    
    def test_convert_unsupported_currency_raises_error(self):
        """Converting with unsupported currency should raise error."""
        money = Money(1000, "USD")
        
        with pytest.raises(ValueError, match="not available"):
            convert_currency(money, "XYZ")
