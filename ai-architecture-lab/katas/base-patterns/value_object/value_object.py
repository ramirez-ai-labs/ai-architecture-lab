"""
Value Object Pattern - Base Implementation

A Value Object is a small immutable object whose equality is based on value,
not identity. Two value objects are equal if they have the same values,
regardless of whether they are the same instance.

Key characteristics:
- Immutable: Once created, cannot be modified
- Equality by value: Two objects with same values are equal
- No identity: Value objects don't have a unique identifier
- Self-validating: Constructor validates and ensures invariants

Examples: Money, Email, DateRange, Address, Color
"""

from abc import ABC, abstractmethod
from typing import Any


class ValueObject(ABC):
    """
    Base class for Value Objects.
    
    Provides:
    - Immutability enforcement
    - Value-based equality
    - Hash support (for use in sets/dicts)
    - String representation
    
    Subclasses must:
    1. Implement `_get_equality_components()` to return tuple of values for comparison
    2. Ensure all attributes are immutable (frozen dataclass or readonly properties)
    """
    
    def __eq__(self, other: Any) -> bool:
        """Two value objects are equal if they have the same type and values."""
        if not isinstance(other, self.__class__):
            return False
        
        return self._get_equality_components() == other._get_equality_components()
    
    def __ne__(self, other: Any) -> bool:
        """Not equal is the inverse of equal."""
        return not self.__eq__(other)
    
    def __hash__(self) -> int:
        """
        Hash is based on the class and equality components.
        This allows value objects to be used in sets and as dictionary keys.
        """
        return hash((self.__class__, self._get_equality_components()))
    
    def __repr__(self) -> str:
        """String representation includes class name and values."""
        components = self._get_equality_components()
        if len(components) == 1:
            return f"{self.__class__.__name__}({components[0]!r})"
        return f"{self.__class__.__name__}{components!r}"
    
    @abstractmethod
    def _get_equality_components(self) -> tuple:
        """
        Return a tuple of values that determine equality.
        
        This method must be implemented by subclasses to specify
        which attributes should be compared for equality.
        
        Returns:
            tuple: Values to compare for equality
        """
        pass
