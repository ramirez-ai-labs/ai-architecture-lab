"""In-memory tabular representation of query results.

WHAT IS RECORD SET?
A Record Set is a lightweight data structure that holds a collection of rows
(records) typically returned from a database query. Unlike a raw list of dicts,
a Record Set provides consistent operations: column access, filtering, and safe
iteration. It's a stable interface between a data-access layer and domain logic,
letting the domain stay ignorant of how data actually arrived (SQL, REST API, etc.).

WHY USE IT?
In production, think of Record Set as what lives in memory after fetch; it's not
the query itself, but the result. It trades simplicity for power: no sorting,
no complex transformations. If you need those, move the logic to your Gateway.

KEY BENEFIT: Defensive Copying
Record Set provides defensive copies of rows when you access them. This means
if you modify a row you retrieved, the original Record Set is unaffected. This
prevents accidental mutations and makes testing easier.

PATTERN RELATIONSHIPS:
This is a foundational pattern that pairs with:
- Table Data Gateway: fetches rows from database, returns Record Set
- Row Data Gateway: returns single rows, often wrapped in Record Set of 1
- Data Mapper: converts Record Set rows to domain objects
"""
from typing import Any, Callable, Dict, List, Optional


class RecordSet:
    """An immutable in-memory collection of rows returned from a query.

    DESIGN APPROACH:
    A Record Set is a thin wrapper around a list of dict rows. Each dict represents
    a single row from a query result. The column names come from the dict keys.
    This keeps the pattern simple and doesn't require upfront schema definition.

    WHAT DOES IT PROVIDE?
    - count(): Get the number of rows
    - row(index): Get a specific row by position
    - column(name): Extract all values for a single column
    - where(predicate): Filter rows by a condition
    - first(): Get the first row
    - is_empty(): Check if there are any rows
    - Iteration: Loop through rows naturally with for loops

    DEFENSIVE COPYING:
    All accessors return copies of rows, not references. This means if you
    modify a row you get back, the original Record Set is not affected.
    This is a key safety feature that prevents accidental bugs.

    SCHEMA FLEXIBILITY:
    Record Set doesn't enforce a schema. Different rows can have different
    column sets. If a row is missing a column, column() returns None for that row.

    EXAMPLE USAGE:
        >>> rows = [
        ...     {"id": 1, "name": "Alice", "age": 30},
        ...     {"id": 2, "name": "Bob", "age": 25},
        ... ]
        >>> record_set = RecordSet(rows)
        >>> record_set.count()
        2
        >>> names = record_set.column("name")
        >>> names
        ['Alice', 'Bob']
        >>> filtered = record_set.where(lambda row: row["age"] > 26)
        >>> filtered.count()
        1
    """

    def __init__(self, rows: List[Dict[str, Any]]):
        """Initialize a Record Set with a list of rows.

        VALIDATION:
        We validate that rows is a list and that every element is a dict.
        This prevents bugs later when we try to access row data.

        DEFENSIVE COPY:
        We make a copy of the input rows list. This means if the caller modifies
        their original list later, it won't affect this Record Set. This is
        important for safety and predictability.

        Args:
            rows: A list of dictionaries, each representing a row. Keys are
                column names (e.g., "id", "name", "age"), values are the cell data.
                Rows do not need to have identical keys; some rows can have
                different columns than others.

        Raises:
            TypeError: If rows is not a list or contains non-dict entries.
                Example: RecordSet("not a list") raises TypeError
                Example: RecordSet([{"id": 1}, "not a dict"]) raises TypeError
        """
        # Check that rows is actually a list
        if not isinstance(rows, list):
            raise TypeError("rows must be a list of dictionaries")

        # Check that every element in rows is a dictionary
        if rows and not all(isinstance(row, dict) for row in rows):
            raise TypeError("all rows must be dictionaries")

        # Make a defensive copy so external changes don't affect this Record Set
        self._rows = list(rows)

    def count(self) -> int:
        """Return the number of rows in this Record Set.

        Returns:
            An integer count of rows.
        """
        return len(self._rows)

    def is_empty(self) -> bool:
        """Return True if the Record Set has no rows.

        Returns:
            True if empty, False otherwise.
        """
        return self.count() == 0

    def column(self, name: str) -> List[Any]:
        """Extract a single column by name from all rows.

        WHAT DOES THIS DO?
        This method is useful when you need all values for a specific column.
        For example, if you want all customer names or all product IDs from
        a query result, you use column() to extract just that one column.

        HANDLING MISSING COLUMNS:
        If some rows are missing the requested column, we return None for those
        rows. This handles heterogeneous data (rows with different columns).

        EXAMPLE:
            >>> record_set = RecordSet([
            ...     {"id": 1, "name": "Alice", "age": 30},
            ...     {"id": 2, "name": "Bob", "age": 25},
            ... ])
            >>> record_set.column("name")
            ['Alice', 'Bob']
            >>> record_set.column("age")
            [30, 25]

        Args:
            name: The column name (dict key) you want to extract.

        Returns:
            A list of values for that column across all rows. If a row is
            missing the column, None is used in its place.

        Raises:
            ValueError: If the Record Set is empty.
            ValueError: If the column name does not appear in ANY row.
        """
        # First check: can't extract from empty Record Set
        if self.is_empty():
            raise ValueError(f"Cannot extract column '{name}' from empty Record Set")

        # Second check: make sure at least one row has this column
        # Otherwise we'd be extracting a column that doesn't exist anywhere
        if not any(name in row for row in self._rows):
            raise ValueError(f"Column '{name}' not found in any row")

        # Extract the column values, using None for rows missing this column
        return [row.get(name) for row in self._rows]

    def row(self, index: int) -> Dict[str, Any]:
        """Get a row by index.

        Args:
            index: Zero-based row index.

        Returns:
            A copy of the row dict at that index.

        Raises:
            IndexError: If index is out of bounds.
        """
        if index < 0 or index >= len(self._rows):
            raise IndexError(f"Row index {index} out of bounds (size: {self.count()})")
        return dict(self._rows[index])

    def rows(self) -> List[Dict[str, Any]]:
        """Get all rows as a list of dicts.

        Returns:
            A defensive copy of the rows list.
        """
        return [dict(r) for r in self._rows]

    def where(self, predicate: Callable[[Dict[str, Any]], bool]) -> "RecordSet":
        """Filter rows by a predicate function (condition).

        WHAT IS A PREDICATE?
        A predicate is a function that takes a row and returns True or False.
        True means "keep this row", False means "filter it out".

        KEY DESIGN DECISION: IMMUTABILITY
        This method returns a NEW Record Set rather than modifying the current
        one. This is important for safety:
        - The original Record Set is unchanged
        - You can chain multiple where() calls without affecting earlier results
        - Tests are easier because Record Sets are predictable

        CHAINING:
        You can chain multiple where() calls to apply multiple filters.
        Example: rs.where(is_active).where(is_expensive).where(is_in_stock)

        EXAMPLES:
            # Simple filtering
            >>> record_set = RecordSet([
            ...     {"id": 1, "age": 30},
            ...     {"id": 2, "age": 25},
            ...     {"id": 3, "age": 35},
            ... ])
            >>> filtered = record_set.where(lambda row: row["age"] > 26)
            >>> filtered.count()
            2

            # Chaining filters
            >>> expensive_and_active = (record_set
            ...     .where(lambda r: r["price"] > 100)
            ...     .where(lambda r: r["active"] is True))

        Args:
            predicate: A callable that takes a row dict and returns True if
                the row should be included in the result, False otherwise.

        Returns:
            A new Record Set containing only the rows where predicate returned True.
            If no rows match, returns an empty Record Set (not None).
        """
        # Apply the predicate to each row
        # Keep only rows where predicate(row) is True
        filtered_rows = [row for row in self._rows if predicate(row)]

        # Return a new Record Set with the filtered rows
        # This preserves immutability: original Record Set is unchanged
        return RecordSet(filtered_rows)

    def first(self) -> Optional[Dict[str, Any]]:
        """Get the first row, or None if empty.

        Returns:
            A copy of the first row, or None if the Record Set is empty.
        """
        if self.is_empty():
            return None
        return dict(self._rows[0])

    def __iter__(self):
        """Iterate over rows as dicts."""
        for row in self._rows:
            yield dict(row)

    def __repr__(self) -> str:
        return f"RecordSet({self.count()} rows)"
