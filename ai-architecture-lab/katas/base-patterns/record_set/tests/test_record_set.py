"""Tests for Record Set pattern."""
import pytest
from record_set import RecordSet


class TestRecordSetInitialization:
    """Tests for Record Set creation and validation."""

    def test_create_empty_record_set(self):
        """Can create an empty Record Set."""
        rs = RecordSet([])
        assert rs.count() == 0
        assert rs.is_empty()

    def test_create_record_set_with_rows(self):
        """Can create a Record Set with rows."""
        rows = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        rs = RecordSet(rows)
        assert rs.count() == 2

    def test_record_set_rejects_non_list(self):
        """Record Set rejects non-list input."""
        with pytest.raises(TypeError):
            RecordSet("not a list")

    def test_record_set_rejects_non_dict_rows(self):
        """Record Set rejects rows that are not dicts."""
        with pytest.raises(TypeError):
            RecordSet([{"id": 1}, "not a dict"])

    def test_record_set_makes_defensive_copy(self):
        """Record Set makes a copy of the input rows list."""
        original = [{"id": 1}]
        rs = RecordSet(original)
        original.append({"id": 2})
        assert rs.count() == 1


class TestRecordSetBasicOperations:
    """Tests for basic Record Set operations."""

    @pytest.fixture
    def sample_rs(self):
        """A Record Set with sample user data."""
        return RecordSet([
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25},
            {"id": 3, "name": "Charlie", "age": 35},
        ])

    def test_count(self, sample_rs):
        """Can get the count of rows."""
        assert sample_rs.count() == 3

    def test_is_empty(self, sample_rs):
        """Can check if Record Set is empty."""
        assert not sample_rs.is_empty()
        empty_rs = RecordSet([])
        assert empty_rs.is_empty()

    def test_row_by_index(self, sample_rs):
        """Can get a row by index."""
        row = sample_rs.row(0)
        assert row["name"] == "Alice"

    def test_row_out_of_bounds(self, sample_rs):
        """Accessing out-of-bounds row raises IndexError."""
        with pytest.raises(IndexError):
            sample_rs.row(10)

    def test_row_negative_index(self, sample_rs):
        """Negative indices raise IndexError (no Python-style indexing)."""
        with pytest.raises(IndexError):
            sample_rs.row(-1)

    def test_row_returns_copy(self, sample_rs):
        """Row method returns a copy, not the original dict."""
        row = sample_rs.row(0)
        row["name"] = "Modified"
        # Original should be unchanged
        first = sample_rs.row(0)
        assert first["name"] == "Alice"

    def test_first(self, sample_rs):
        """Can get the first row."""
        row = sample_rs.first()
        assert row["name"] == "Alice"

    def test_first_empty(self):
        """First on empty Record Set returns None."""
        rs = RecordSet([])
        assert rs.first() is None

    def test_rows(self, sample_rs):
        """Can get all rows as a list."""
        all_rows = sample_rs.rows()
        assert len(all_rows) == 3
        assert all_rows[0]["name"] == "Alice"

    def test_rows_returns_copies(self, sample_rs):
        """Rows method returns copies."""
        all_rows = sample_rs.rows()
        all_rows[0]["name"] = "Modified"
        # Original should be unchanged
        first = sample_rs.row(0)
        assert first["name"] == "Alice"


class TestRecordSetColumn:
    """Tests for column extraction."""

    @pytest.fixture
    def sample_rs(self):
        return RecordSet([
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25},
            {"id": 3, "name": "Charlie", "age": 35},
        ])

    def test_extract_column(self, sample_rs):
        """Can extract a column by name."""
        names = sample_rs.column("name")
        assert names == ["Alice", "Bob", "Charlie"]

    def test_extract_column_missing_in_all_rows(self, sample_rs):
        """Extracting non-existent column raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            sample_rs.column("email")

    def test_extract_column_empty_record_set(self):
        """Extracting column from empty Record Set raises ValueError."""
        rs = RecordSet([])
        with pytest.raises(ValueError):
            rs.column("name")

    def test_extract_column_with_missing_keys(self):
        """Column extraction uses None for missing keys."""
        rs = RecordSet([
            {"id": 1, "name": "Alice"},
            {"id": 2},  # Missing 'name' key
            {"id": 3, "name": "Charlie"},
        ])
        names = rs.column("name")
        assert names == ["Alice", None, "Charlie"]


class TestRecordSetFiltering:
    """Tests for filtering with where() predicate."""

    @pytest.fixture
    def sample_rs(self):
        return RecordSet([
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25},
            {"id": 3, "name": "Charlie", "age": 35},
        ])

    def test_filter_by_predicate(self, sample_rs):
        """Can filter rows with a predicate."""
        filtered = sample_rs.where(lambda r: r["age"] > 26)
        assert filtered.count() == 2
        names = filtered.column("name")
        assert names == ["Alice", "Charlie"]

    def test_filter_returns_new_record_set(self, sample_rs):
        """Filter returns a new Record Set."""
        filtered = sample_rs.where(lambda r: r["age"] > 26)
        assert isinstance(filtered, RecordSet)
        # Original is unchanged
        assert sample_rs.count() == 3

    def test_filter_no_matches(self, sample_rs):
        """Filter with no matching rows returns empty Record Set."""
        filtered = sample_rs.where(lambda r: r["age"] > 100)
        assert filtered.is_empty()

    def test_filter_all_match(self, sample_rs):
        """Filter where all rows match returns full Record Set."""
        filtered = sample_rs.where(lambda r: r["age"] > 0)
        assert filtered.count() == 3

    def test_chained_filters(self, sample_rs):
        """Can chain multiple filter calls."""
        filtered = (sample_rs
                    .where(lambda r: r["age"] > 24)
                    .where(lambda r: r["name"].startswith("A") or r["name"].startswith("C")))
        assert filtered.count() == 2
        names = filtered.column("name")
        assert set(names) == {"Alice", "Charlie"}

    def test_filter_with_string_predicate(self):
        """Can filter using string column matching."""
        rs = RecordSet([
            {"id": 1, "status": "active"},
            {"id": 2, "status": "inactive"},
            {"id": 3, "status": "active"},
        ])
        active = rs.where(lambda r: r["status"] == "active")
        assert active.count() == 2


class TestRecordSetIteration:
    """Tests for iteration over Record Set."""

    def test_iterate_over_record_set(self):
        """Can iterate over Record Set rows."""
        rs = RecordSet([
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ])
        names = [row["name"] for row in rs]
        assert names == ["Alice", "Bob"]

    def test_iteration_yields_copies(self):
        """Iteration yields copies, not references."""
        rs = RecordSet([{"id": 1, "name": "Alice"}])
        for row in rs:
            row["name"] = "Modified"
        # Original unchanged
        original_row = rs.row(0)
        assert original_row["name"] == "Alice"


class TestRecordSetEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_record_set_with_heterogeneous_rows(self):
        """Record Set can handle rows with different column sets."""
        rs = RecordSet([
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob"},  # No age
            {"id": 3, "email": "charlie@example.com", "age": 35},  # No name
        ])
        assert rs.count() == 3
        # Column extraction uses None for missing values
        ages = rs.column("age")
        assert ages == [30, None, 35]

    def test_record_set_with_empty_dicts(self):
        """Record Set can contain empty row dicts."""
        rs = RecordSet([{}, {"id": 1}, {}])
        assert rs.count() == 3

    def test_repr(self):
        """Record Set has a readable repr."""
        rs = RecordSet([{"id": 1}, {"id": 2}])
        assert repr(rs) == "RecordSet(2 rows)"
