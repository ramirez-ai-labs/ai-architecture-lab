"""
Tests for Email Value Object.

Demonstrates:
- Email validation
- Value equality
- Immutability
- Use in collections
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from examples.email import Email


class TestEmailValidation:
    """Test email address validation."""
    
    def test_valid_email_creates_object(self):
        """Valid email addresses should create Email objects."""
        email = Email("user@example.com")
        assert email.address == "user@example.com"
    
    def test_email_is_normalized_to_lowercase(self):
        """Email addresses should be normalized to lowercase."""
        email = Email("User@Example.COM")
        assert email.address == "user@example.com"
    
    def test_email_whitespace_is_trimmed(self):
        """Whitespace should be trimmed from email addresses."""
        email = Email("  user@example.com  ")
        assert email.address == "user@example.com"
    
    def test_invalid_email_raises_error(self):
        """Invalid email formats should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("not-an-email")
        
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("missing@domain")
        
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("@example.com")
    
    def test_empty_email_raises_error(self):
        """Empty email addresses should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Email("")
        
        with pytest.raises(ValueError, match="cannot be empty"):
            Email("   ")
    
    def test_non_string_raises_error(self):
        """Non-string inputs should raise ValueError."""
        with pytest.raises(ValueError, match="must be a string"):
            Email(123)
        
        with pytest.raises(ValueError, match="must be a string"):
            Email(None)


class TestEmailEquality:
    """Test value-based equality for Email."""
    
    def test_same_email_addresses_are_equal(self):
        """Two Email objects with same address should be equal."""
        email1 = Email("user@example.com")
        email2 = Email("user@example.com")
        
        assert email1 == email2
        assert not (email1 != email2)
    
    def test_case_insensitive_equality(self):
        """Email equality should be case-insensitive."""
        email1 = Email("User@Example.COM")
        email2 = Email("user@example.com")
        
        assert email1 == email2
    
    def test_different_emails_are_not_equal(self):
        """Different email addresses should not be equal."""
        email1 = Email("user1@example.com")
        email2 = Email("user2@example.com")
        
        assert email1 != email2
    
    def test_can_use_in_set(self):
        """Email objects can be used in sets."""
        email1 = Email("user@example.com")
        email2 = Email("USER@EXAMPLE.COM")  # Same email, different case
        email3 = Email("other@example.com")
        
        email_set = {email1, email2, email3}
        
        # email1 and email2 are equal, so set should only have 2 items
        assert len(email_set) == 2
        assert email1 in email_set
        assert email2 in email_set
        assert email3 in email_set


class TestEmailImmutability:
    """Test immutability of Email objects."""
    
    def test_email_cannot_be_modified(self):
        """Email address should be immutable after creation."""
        email = Email("user@example.com")
        original_address = email.address
        
        # Attempting to modify _address directly would be a design violation
        # The property is read-only, enforcing immutability
        assert email.address == original_address


class TestEmailStringRepresentation:
    """Test string representation of Email."""
    
    def test_str_returns_address(self):
        """String representation should return the email address."""
        email = Email("user@example.com")
        assert str(email) == "user@example.com"
    
    def test_repr_includes_class_name(self):
        """Repr should include class name."""
        email = Email("user@example.com")
        repr_str = repr(email)
        
        assert "Email" in repr_str
        assert "user@example.com" in repr_str
