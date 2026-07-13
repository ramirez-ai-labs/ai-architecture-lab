"""
Currency Conversion Example

Demonstrates how to handle currency conversion in the Money value object.
Note: This is a simplified example. Real applications would use
live exchange rates from an API.
"""

import sys
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from money import Money


# Simplified exchange rates (for demonstration only)
# In production, fetch from an API
EXCHANGE_RATES = {
    "USD": {
        "EUR": 0.85,
        "GBP": 0.73,
        "JPY": 110.0,
    },
    "EUR": {
        "USD": 1.18,
        "GBP": 0.86,
        "JPY": 129.0,
    },
    "GBP": {
        "USD": 1.37,
        "EUR": 1.16,
        "JPY": 150.0,
    },
    "JPY": {
        "USD": 0.0091,
        "EUR": 0.0078,
        "GBP": 0.0067,
    },
}


def convert_currency(money: Money, target_currency: str) -> Money:
    """
    Convert Money from one currency to another.
    
    Args:
        money: Money object to convert
        target_currency: Target currency code
        
    Returns:
        New Money object in target currency
        
    Raises:
        ValueError: If conversion rate not available
    """
    if money.currency == target_currency:
        return money
    
    if money.currency not in EXCHANGE_RATES:
        raise ValueError(f"Exchange rate not available for {money.currency}")
    
    if target_currency not in EXCHANGE_RATES[money.currency]:
        raise ValueError(
            f"Exchange rate from {money.currency} to {target_currency} not available"
        )
    
    # Get exchange rate
    rate = EXCHANGE_RATES[money.currency][target_currency]
    
    # Convert: multiply by rate and round to nearest cent
    # For JPY, we need to handle differently (no decimal places)
    if target_currency == "JPY":
        # Convert to JPY (multiply by 100 since JPY doesn't use cents)
        jpy_amount = round(money.amount_cents * rate / 100)
        return Money(jpy_amount, target_currency)
    else:
        # Convert to other currencies (standard conversion)
        target_cents = round(money.amount_cents * rate)
        return Money(target_cents, target_currency)


# Example usage
if __name__ == "__main__":
    # Create money in USD
    usd_money = Money(1000, "USD")  # $10.00
    print(f"Original: {usd_money}")
    
    # Convert to EUR
    eur_money = convert_currency(usd_money, "EUR")
    print(f"Converted to EUR: {eur_money}")
    
    # Convert to GBP
    gbp_money = convert_currency(usd_money, "GBP")
    print(f"Converted to GBP: {gbp_money}")
