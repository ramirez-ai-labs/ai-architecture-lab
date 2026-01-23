"""
Email Value Object Example

Demonstrates a Value Object for email addresses with validation.
"""

import re
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from value_object import ValueObject


class Email(ValueObject):
    """
    Email address as a Value Object.
    
    Characteristics:
    - Immutable: Once created, email cannot be changed
    - Self-validating: Constructor validates email format
    - Value equality: Two Email objects with same address are equal
    """
    
    # Simple email regex (for demonstration - production would use more robust validation)
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    def __init__(self, address: str):
        """
        Create an Email value object.
        
        Args:
            address: Email address string
            
        Raises:
            ValueError: If email format is invalid
        """
        if not isinstance(address, str):
            raise ValueError("Email address must be a string")
        
        address = address.strip().lower()
        
        if not address:
            raise ValueError("Email address cannot be empty")
        
        if not self.EMAIL_PATTERN.match(address):
            raise ValueError(f"Invalid email format: {address}")
        
        # Store as private attribute to enforce immutability
        self._address = address
    
    @property
    def address(self) -> str:
        """Get the email address (read-only)."""
        return self._address
    
    def _get_equality_components(self) -> tuple:
        """Email equality is based on the address value."""
        return (self._address,)
    
    def __str__(self) -> str:
        """String representation returns the email address."""
        return self._address
