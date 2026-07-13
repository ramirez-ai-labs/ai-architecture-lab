"""
Tests for Table Data Gateway.

Demonstrates:
- Gateway creation and initialization
- CRUD operations (Create, Read, Update, Delete)
- Table-level operations
- Error handling
"""

import pytest
import sqlite3
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from table_data_gateway.table_data_gateway import TableDataGateway


def create_test_table(connection: sqlite3.Connection, table_name: str = "test_table"):
    """
    Create a test table for testing.
    
    Args:
        connection: SQLite database connection
        table_name: Name of the table to create
    """
    cursor = connection.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value INTEGER NOT NULL
        )
    """)
    connection.commit()
    cursor.close()


@pytest.fixture
def db_connection():
    """Create an in-memory SQLite database for testing."""
    connection = sqlite3.connect(":memory:")
    create_test_table(connection)
    yield connection
    connection.close()


@pytest.fixture
def gateway(db_connection):
    """Create a TableDataGateway for testing."""
    return TableDataGateway(db_connection, "test_table")


class TestTableDataGatewayCreation:
    """Test gateway creation and initialization."""
    
    def test_create_gateway_with_valid_connection_and_table(self, db_connection):
        """Valid connection and table name should create gateway."""
        gateway = TableDataGateway(db_connection, "test_table")
        
        assert gateway.table_name == "test_table"
    
    def test_invalid_connection_raises_error(self):
        """Invalid connection should raise ValueError."""
        with pytest.raises(ValueError, match="must be a sqlite3.Connection"):
            TableDataGateway("not a connection", "test_table")
    
    def test_empty_table_name_raises_error(self, db_connection):
        """Empty table name should raise ValueError."""
        with pytest.raises(ValueError, match="must be a non-empty string"):
            TableDataGateway(db_connection, "")
    
    def test_non_string_table_name_raises_error(self, db_connection):
        """Non-string table name should raise ValueError."""
        with pytest.raises(ValueError, match="must be a non-empty string"):
            TableDataGateway(db_connection, 123)


class TestTableDataGatewayInsert:
    """Test insert operations."""
    
    def test_insert_creates_new_row(self, gateway):
        """Insert should create a new row and return ID."""
        row_id = gateway.insert({"name": "Test", "value": 42})
        
        assert isinstance(row_id, int)
        assert row_id > 0
    
    def test_inserted_row_can_be_retrieved(self, gateway):
        """Inserted row should be retrievable."""
        row_id = gateway.insert({"name": "Test", "value": 42})
        
        row = gateway.find_by_id(row_id)
        
        assert row is not None
        assert row["name"] == "Test"
        assert row["value"] == 42
    
    def test_insert_empty_data_raises_error(self, gateway):
        """Insert with empty data should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            gateway.insert({})
    
    def test_insert_non_dict_raises_error(self, gateway):
        """Insert with non-dict should raise ValueError."""
        with pytest.raises(ValueError, match="must be a dictionary"):
            gateway.insert("not a dict")


class TestTableDataGatewayFind:
    """Test find operations."""
    
    def test_find_all_returns_all_rows(self, gateway):
        """find_all() should return all rows in table."""
        gateway.insert({"name": "Row 1", "value": 10})
        gateway.insert({"name": "Row 2", "value": 20})
        
        all_rows = gateway.find_all()
        
        assert len(all_rows) == 2
        assert all_rows[0]["name"] in ["Row 1", "Row 2"]
        assert all_rows[1]["name"] in ["Row 1", "Row 2"]
    
    def test_find_all_returns_empty_list_when_table_empty(self, gateway):
        """find_all() should return empty list when table is empty."""
        all_rows = gateway.find_all()
        
        assert all_rows == []
    
    def test_find_by_id_returns_correct_row(self, gateway):
        """find_by_id() should return the correct row."""
        row_id = gateway.insert({"name": "Test", "value": 42})
        
        row = gateway.find_by_id(row_id)
        
        assert row is not None
        assert row["id"] == row_id
        assert row["name"] == "Test"
        assert row["value"] == 42
    
    def test_find_by_id_returns_none_when_not_found(self, gateway):
        """find_by_id() should return None when row doesn't exist."""
        row = gateway.find_by_id(999)
        
        assert row is None
    
    def test_find_all_returns_list_of_dicts(self, gateway):
        """find_all() should return list of dictionaries."""
        gateway.insert({"name": "Test", "value": 42})
        
        all_rows = gateway.find_all()
        
        assert isinstance(all_rows, list)
        assert len(all_rows) > 0
        assert isinstance(all_rows[0], dict)


class TestTableDataGatewayUpdate:
    """Test update operations."""
    
    def test_update_modifies_existing_row(self, gateway):
        """update() should modify existing row."""
        row_id = gateway.insert({"name": "Original", "value": 10})
        
        updated = gateway.update(row_id, {"name": "Updated", "value": 20})
        
        assert updated is True
        
        row = gateway.find_by_id(row_id)
        assert row["name"] == "Updated"
        assert row["value"] == 20
    
    def test_update_returns_false_when_row_not_found(self, gateway):
        """update() should return False when row doesn't exist."""
        updated = gateway.update(999, {"name": "Test"})
        
        assert updated is False
    
    def test_update_partial_data(self, gateway):
        """update() should allow updating only some columns."""
        row_id = gateway.insert({"name": "Original", "value": 10})
        
        gateway.update(row_id, {"value": 20})
        
        row = gateway.find_by_id(row_id)
        assert row["name"] == "Original"  # Unchanged
        assert row["value"] == 20  # Updated
    
    def test_update_empty_data_raises_error(self, gateway):
        """update() with empty data should raise ValueError."""
        row_id = gateway.insert({"name": "Test", "value": 10})
        
        with pytest.raises(ValueError, match="cannot be empty"):
            gateway.update(row_id, {})
    
    def test_update_non_dict_raises_error(self, gateway):
        """update() with non-dict should raise ValueError."""
        row_id = gateway.insert({"name": "Test", "value": 10})
        
        with pytest.raises(ValueError, match="must be a dictionary"):
            gateway.update(row_id, "not a dict")


class TestTableDataGatewayDelete:
    """Test delete operations."""
    
    def test_delete_removes_row(self, gateway):
        """delete() should remove row from table."""
        row_id = gateway.insert({"name": "Test", "value": 42})
        
        deleted = gateway.delete(row_id)
        
        assert deleted is True
        
        row = gateway.find_by_id(row_id)
        assert row is None
    
    def test_delete_returns_false_when_row_not_found(self, gateway):
        """delete() should return False when row doesn't exist."""
        deleted = gateway.delete(999)
        
        assert deleted is False
    
    def test_delete_reduces_count(self, gateway):
        """delete() should reduce the row count."""
        row_id1 = gateway.insert({"name": "Row 1", "value": 10})
        row_id2 = gateway.insert({"name": "Row 2", "value": 20})
        
        initial_count = gateway.count()
        gateway.delete(row_id1)
        final_count = gateway.count()
        
        assert final_count == initial_count - 1


class TestTableDataGatewayCount:
    """Test count operations."""
    
    def test_count_returns_zero_for_empty_table(self, gateway):
        """count() should return 0 for empty table."""
        count = gateway.count()
        
        assert count == 0
    
    def test_count_returns_correct_number(self, gateway):
        """count() should return correct number of rows."""
        gateway.insert({"name": "Row 1", "value": 10})
        gateway.insert({"name": "Row 2", "value": 20})
        gateway.insert({"name": "Row 3", "value": 30})
        
        count = gateway.count()
        
        assert count == 3
    
    def test_count_updates_after_insert(self, gateway):
        """count() should update after insert."""
        initial_count = gateway.count()
        
        gateway.insert({"name": "New Row", "value": 10})
        
        new_count = gateway.count()
        assert new_count == initial_count + 1
    
    def test_count_updates_after_delete(self, gateway):
        """count() should update after delete."""
        row_id = gateway.insert({"name": "Row", "value": 10})
        initial_count = gateway.count()
        
        gateway.delete(row_id)
        
        final_count = gateway.count()
        assert final_count == initial_count - 1
