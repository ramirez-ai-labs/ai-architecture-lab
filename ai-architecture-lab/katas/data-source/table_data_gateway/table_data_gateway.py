"""
Table Data Gateway Pattern

A gateway object that encapsulates all access to a database table.

Key characteristics:
- One gateway per table
- Encapsulates SQL for table operations
- Returns simple data structures (dicts, tuples, or simple objects)
- Hides database details from domain logic
- Provides table-level CRUD operations

Why use Table Data Gateway?
- Separates database access from business logic
- Makes database changes easier (change gateway, not domain)
- Simplifies testing (can mock gateway)
- Reduces SQL duplication across application
"""

import sqlite3
from typing import List, Dict, Optional, Any
from contextlib import contextmanager


class TableDataGateway:
    """
    Gateway object encapsulating all access to a database table.
    
    This gateway provides table-level CRUD operations:
    - find_all(): Get all rows
    - find_by_id(): Get row by ID
    - insert(): Create new row
    - update(): Update existing row
    - delete(): Delete row
    
    Characteristics:
    - One gateway per table
    - Encapsulates SQL queries
    - Returns simple data structures (dicts)
    - Hides database connection details
    """
    
    def __init__(self, connection: sqlite3.Connection, table_name: str):
        """
        Initialize Table Data Gateway.
        
        Args:
            connection: SQLite database connection
            table_name: Name of the table this gateway manages
        """
        if not isinstance(connection, sqlite3.Connection):
            raise ValueError("connection must be a sqlite3.Connection")
        
        if not isinstance(table_name, str) or not table_name:
            raise ValueError("table_name must be a non-empty string")
        
        self._connection = connection
        self._table_name = table_name
    
    @property
    def table_name(self) -> str:
        """Get the table name (read-only)."""
        return self._table_name
    
    def find_all(self) -> List[Dict[str, Any]]:
        """
        Find all rows in the table.
        
        Returns:
            List of dictionaries, each representing a row
        """
        query = f"SELECT * FROM {self._table_name}"
        cursor = self._connection.cursor()
        cursor.execute(query)
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        # Convert rows to dictionaries
        rows = []
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            rows.append(row_dict)
        
        cursor.close()
        return rows
    
    def find_by_id(self, row_id: int) -> Optional[Dict[str, Any]]:
        """
        Find a row by its ID.
        
        Args:
            row_id: The ID of the row to find
            
        Returns:
            Dictionary representing the row, or None if not found
        """
        query = f"SELECT * FROM {self._table_name} WHERE id = ?"
        cursor = self._connection.cursor()
        cursor.execute(query, (row_id,))
        
        row = cursor.fetchone()
        cursor.close()
        
        if row is None:
            return None
        
        # Get column names
        cursor = self._connection.cursor()
        cursor.execute(f"SELECT * FROM {self._table_name} LIMIT 0")
        columns = [description[0] for description in cursor.description]
        cursor.close()
        
        # Convert row to dictionary
        return dict(zip(columns, row))
    
    def insert(self, data: Dict[str, Any]) -> int:
        """
        Insert a new row into the table.
        
        Args:
            data: Dictionary of column names to values
            
        Returns:
            The ID of the newly inserted row
        """
        if not isinstance(data, dict):
            raise ValueError("data must be a dictionary")
        
        if not data:
            raise ValueError("data cannot be empty")
        
        # Build INSERT query
        columns = list(data.keys())
        placeholders = ", ".join(["?" for _ in columns])
        column_names = ", ".join(columns)
        
        query = f"INSERT INTO {self._table_name} ({column_names}) VALUES ({placeholders})"
        values = tuple(data.values())
        
        cursor = self._connection.cursor()
        cursor.execute(query, values)
        self._connection.commit()
        
        row_id = cursor.lastrowid
        cursor.close()
        
        return row_id
    
    def update(self, row_id: int, data: Dict[str, Any]) -> bool:
        """
        Update an existing row in the table.
        
        Args:
            row_id: The ID of the row to update
            data: Dictionary of column names to new values
            
        Returns:
            True if row was updated, False if row not found
        """
        if not isinstance(data, dict):
            raise ValueError("data must be a dictionary")
        
        if not data:
            raise ValueError("data cannot be empty")
        
        # Check if row exists
        existing = self.find_by_id(row_id)
        if existing is None:
            return False
        
        # Build UPDATE query
        set_clauses = [f"{column} = ?" for column in data.keys()]
        set_clause = ", ".join(set_clauses)
        values = tuple(data.values()) + (row_id,)
        
        query = f"UPDATE {self._table_name} SET {set_clause} WHERE id = ?"
        
        cursor = self._connection.cursor()
        cursor.execute(query, values)
        self._connection.commit()
        
        rows_affected = cursor.rowcount
        cursor.close()
        
        return rows_affected > 0
    
    def delete(self, row_id: int) -> bool:
        """
        Delete a row from the table.
        
        Args:
            row_id: The ID of the row to delete
            
        Returns:
            True if row was deleted, False if row not found
        """
        # Check if row exists
        existing = self.find_by_id(row_id)
        if existing is None:
            return False
        
        query = f"DELETE FROM {self._table_name} WHERE id = ?"
        
        cursor = self._connection.cursor()
        cursor.execute(query, (row_id,))
        self._connection.commit()
        
        rows_affected = cursor.rowcount
        cursor.close()
        
        return rows_affected > 0
    
    def count(self) -> int:
        """
        Count the number of rows in the table.
        
        Returns:
            Number of rows in the table
        """
        query = f"SELECT COUNT(*) FROM {self._table_name}"
        cursor = self._connection.cursor()
        cursor.execute(query)
        
        count = cursor.fetchone()[0]
        cursor.close()
        
        return count
