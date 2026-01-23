"""
Tests for DateRange Value Object.

Demonstrates:
- Date range validation
- Value equality
- Business logic methods
- Use in collections
"""

import pytest
import sys
from pathlib import Path
from datetime import date, timedelta

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from examples.date_range import DateRange


class TestDateRangeValidation:
    """Test date range validation."""
    
    def test_valid_range_creates_object(self):
        """Valid date ranges should create DateRange objects."""
        start = date(2024, 1, 1)
        end = date(2024, 1, 31)
        date_range = DateRange(start, end)
        
        assert date_range.start_date == start
        assert date_range.end_date == end
    
    def test_same_start_and_end_is_valid(self):
        """A range with same start and end date is valid (single day)."""
        single_date = date(2024, 1, 15)
        date_range = DateRange(single_date, single_date)
        
        assert date_range.start_date == single_date
        assert date_range.end_date == single_date
    
    def test_invalid_range_raises_error(self):
        """Start date after end date should raise ValueError."""
        start = date(2024, 1, 31)
        end = date(2024, 1, 1)
        
        with pytest.raises(ValueError, match="cannot be after"):
            DateRange(start, end)
    
    def test_non_date_start_raises_error(self):
        """Non-date start should raise ValueError."""
        with pytest.raises(ValueError, match="must be a date object"):
            DateRange("2024-01-01", date(2024, 1, 31))
    
    def test_non_date_end_raises_error(self):
        """Non-date end should raise ValueError."""
        with pytest.raises(ValueError, match="must be a date object"):
            DateRange(date(2024, 1, 1), "2024-01-31")


class TestDateRangeEquality:
    """Test value-based equality for DateRange."""
    
    def test_same_dates_are_equal(self):
        """Two DateRange objects with same dates should be equal."""
        start = date(2024, 1, 1)
        end = date(2024, 1, 31)
        
        range1 = DateRange(start, end)
        range2 = DateRange(start, end)
        
        assert range1 == range2
        assert not (range1 != range2)
    
    def test_different_dates_are_not_equal(self):
        """Different date ranges should not be equal."""
        range1 = DateRange(date(2024, 1, 1), date(2024, 1, 31))
        range2 = DateRange(date(2024, 2, 1), date(2024, 2, 28))
        
        assert range1 != range2
    
    def test_can_use_in_set(self):
        """DateRange objects can be used in sets."""
        range1 = DateRange(date(2024, 1, 1), date(2024, 1, 31))
        range2 = DateRange(date(2024, 1, 1), date(2024, 1, 31))  # Same as range1
        range3 = DateRange(date(2024, 2, 1), date(2024, 2, 28))
        
        range_set = {range1, range2, range3}
        
        # range1 and range2 are equal, so set should only have 2 items
        assert len(range_set) == 2


class TestDateRangeBusinessLogic:
    """Test business logic methods of DateRange."""
    
    def test_contains_start_date(self):
        """Range should contain its start date."""
        date_range = DateRange(date(2024, 1, 1), date(2024, 1, 31))
        
        assert date_range.contains(date(2024, 1, 1))
    
    def test_contains_end_date(self):
        """Range should contain its end date."""
        date_range = DateRange(date(2024, 1, 1), date(2024, 1, 31))
        
        assert date_range.contains(date(2024, 1, 31))
    
    def test_contains_middle_date(self):
        """Range should contain dates in the middle."""
        date_range = DateRange(date(2024, 1, 1), date(2024, 1, 31))
        
        assert date_range.contains(date(2024, 1, 15))
    
    def test_does_not_contain_before_start(self):
        """Range should not contain dates before start."""
        date_range = DateRange(date(2024, 1, 1), date(2024, 1, 31))
        
        assert not date_range.contains(date(2023, 12, 31))
    
    def test_does_not_contain_after_end(self):
        """Range should not contain dates after end."""
        date_range = DateRange(date(2024, 1, 1), date(2024, 1, 31))
        
        assert not date_range.contains(date(2024, 2, 1))
    
    def test_overlaps_when_ranges_share_dates(self):
        """Ranges should overlap when they share dates."""
        range1 = DateRange(date(2024, 1, 1), date(2024, 1, 31))
        range2 = DateRange(date(2024, 1, 15), date(2024, 2, 15))
        
        assert range1.overlaps(range2)
        assert range2.overlaps(range1)
    
    def test_overlaps_when_one_contains_other(self):
        """Ranges should overlap when one contains the other."""
        range1 = DateRange(date(2024, 1, 1), date(2024, 3, 31))
        range2 = DateRange(date(2024, 2, 1), date(2024, 2, 28))
        
        assert range1.overlaps(range2)
        assert range2.overlaps(range1)
    
    def test_no_overlap_when_ranges_are_separate(self):
        """Ranges should not overlap when they are separate."""
        range1 = DateRange(date(2024, 1, 1), date(2024, 1, 31))
        range2 = DateRange(date(2024, 3, 1), date(2024, 3, 31))
        
        assert not range1.overlaps(range2)
        assert not range2.overlaps(range1)
    
    def test_duration_for_single_day(self):
        """Single day range should have duration of 1."""
        date_range = DateRange(date(2024, 1, 15), date(2024, 1, 15))
        
        assert date_range.duration_days() == 1
    
    def test_duration_for_month(self):
        """January 2024 should have duration of 31 days."""
        date_range = DateRange(date(2024, 1, 1), date(2024, 1, 31))
        
        assert date_range.duration_days() == 31
    
    def test_duration_includes_both_endpoints(self):
        """Duration should include both start and end dates."""
        date_range = DateRange(date(2024, 1, 1), date(2024, 1, 2))
        
        assert date_range.duration_days() == 2


class TestDateRangeStringRepresentation:
    """Test string representation of DateRange."""
    
    def test_str_shows_date_range(self):
        """String representation should show the date range."""
        date_range = DateRange(date(2024, 1, 1), date(2024, 1, 31))
        str_repr = str(date_range)
        
        assert "2024-01-01" in str_repr
        assert "2024-01-31" in str_repr
