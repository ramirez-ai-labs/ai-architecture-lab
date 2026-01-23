"""
DateRange Value Object Example

Demonstrates a Value Object for date ranges with validation.
"""

from datetime import date
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from value_object import ValueObject


class DateRange(ValueObject):
    """
    Date range as a Value Object.
    
    Characteristics:
    - Immutable: Once created, dates cannot be changed
    - Self-validating: Constructor ensures start <= end
    - Value equality: Two DateRange objects with same dates are equal
    - Business logic: Methods like contains(), overlaps(), duration()
    """
    
    def __init__(self, start_date: date, end_date: date):
        """
        Create a DateRange value object.
        
        Args:
            start_date: Start date of the range
            end_date: End date of the range
            
        Raises:
            ValueError: If start_date is after end_date
        """
        if not isinstance(start_date, date):
            raise ValueError("start_date must be a date object")
        
        if not isinstance(end_date, date):
            raise ValueError("end_date must be a date object")
        
        if start_date > end_date:
            raise ValueError(
                f"start_date ({start_date}) cannot be after end_date ({end_date})"
            )
        
        # Store as private attributes to enforce immutability
        self._start_date = start_date
        self._end_date = end_date
    
    @property
    def start_date(self) -> date:
        """Get the start date (read-only)."""
        return self._start_date
    
    @property
    def end_date(self) -> date:
        """Get the end date (read-only)."""
        return self._end_date
    
    def _get_equality_components(self) -> tuple:
        """DateRange equality is based on both dates."""
        return (self._start_date, self._end_date)
    
    def contains(self, check_date: date) -> bool:
        """
        Check if a date falls within this range.
        
        Args:
            check_date: Date to check
            
        Returns:
            bool: True if date is within range (inclusive)
        """
        return self._start_date <= check_date <= self._end_date
    
    def overlaps(self, other: 'DateRange') -> bool:
        """
        Check if this date range overlaps with another.
        
        Args:
            other: Another DateRange to check
            
        Returns:
            bool: True if ranges overlap
        """
        return (
            self.contains(other.start_date) or
            self.contains(other.end_date) or
            other.contains(self.start_date) or
            other.contains(self.end_date)
        )
    
    def duration_days(self) -> int:
        """
        Calculate the duration of the range in days.
        
        Returns:
            int: Number of days in the range (inclusive)
        """
        return (self._end_date - self._start_date).days + 1
    
    def __str__(self) -> str:
        """String representation shows the date range."""
        return f"{self._start_date} to {self._end_date}"
