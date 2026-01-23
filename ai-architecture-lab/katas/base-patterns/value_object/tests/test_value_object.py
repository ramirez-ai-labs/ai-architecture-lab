"""
Tests for Value Object base class.

These tests demonstrate the core characteristics of Value Objects:
- Immutability
- Value-based equality
- Hash support
- String representation
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from value_object import ValueObject


class SimpleValueObject(ValueObject):
    """Simple test implementation of ValueObject."""
    
    def __init__(self, value: int):
        self._value = value
    
    @property
    def value(self) -> int:
        return self._value
    
    def _get_equality_components(self) -> tuple:
        return (self._value,)


class TestValueObjectEquality:
    """Test value-based equality."""
    
    def test_same_values_are_equal(self):
        """Two value objects with same values should be equal."""
        obj1 = SimpleValueObject(42)
        obj2 = SimpleValueObject(42)
        
        assert obj1 == obj2
        assert not (obj1 != obj2)
    
    def test_different_values_are_not_equal(self):
        """Two value objects with different values should not be equal."""
        obj1 = SimpleValueObject(42)
        obj2 = SimpleValueObject(43)
        
        assert obj1 != obj2
        assert not (obj1 == obj2)
    
    def test_different_types_are_not_equal(self):
        """Value objects of different types are never equal."""
        obj1 = SimpleValueObject(42)
        obj2 = "not a value object"
        
        assert obj1 != obj2
        assert not (obj1 == obj2)


class TestValueObjectHash:
    """Test hash support for use in sets and dicts."""
    
    def test_equal_objects_have_same_hash(self):
        """Equal value objects must have the same hash."""
        obj1 = SimpleValueObject(42)
        obj2 = SimpleValueObject(42)
        
        assert hash(obj1) == hash(obj2)
    
    def test_can_use_in_set(self):
        """Value objects can be used in sets (no duplicates by value)."""
        obj1 = SimpleValueObject(42)
        obj2 = SimpleValueObject(42)
        obj3 = SimpleValueObject(43)
        
        value_set = {obj1, obj2, obj3}
        
        # obj1 and obj2 are equal, so set should only have 2 items
        assert len(value_set) == 2
        assert obj1 in value_set
        assert obj2 in value_set
        assert obj3 in value_set
    
    def test_can_use_as_dict_key(self):
        """Value objects can be used as dictionary keys."""
        obj1 = SimpleValueObject(42)
        obj2 = SimpleValueObject(42)
        obj3 = SimpleValueObject(43)
        
        value_dict = {obj1: "first", obj3: "third"}
        
        # obj2 should access the same value as obj1 (they're equal)
        assert value_dict[obj2] == "first"
        assert value_dict[obj3] == "third"
        assert len(value_dict) == 2


class TestValueObjectImmutability:
    """Test immutability characteristics."""
    
    def test_cannot_modify_after_creation(self):
        """Value objects should be immutable after creation."""
        obj = SimpleValueObject(42)
        
        # Attempting to modify should be prevented by design
        # (Python doesn't enforce this, but the pattern does)
        # In practice, attributes should be private and only exposed via properties
        
        # This test documents the expected behavior
        original_value = obj.value
        assert original_value == 42
        
        # If someone tries to modify _value directly, it's a design violation
        # but Python won't prevent it. The pattern encourages immutability.


class TestValueObjectRepresentation:
    """Test string representation."""
    
    def test_repr_includes_class_and_values(self):
        """String representation should include class name and values."""
        obj = SimpleValueObject(42)
        repr_str = repr(obj)
        
        assert "SimpleValueObject" in repr_str
        assert "42" in repr_str
    
    def test_repr_for_single_value(self):
        """Single value objects have clean representation."""
        obj = SimpleValueObject(42)
        repr_str = repr(obj)
        
        # Should be something like: SimpleValueObject(42)
        assert repr_str.startswith("SimpleValueObject(")
        assert "42" in repr_str
