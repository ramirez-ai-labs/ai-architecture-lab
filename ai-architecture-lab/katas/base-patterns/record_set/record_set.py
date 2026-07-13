"""In-memory tabular representation of query results.

A Record Set is a lightweight data structure that holds a collection of rows
(records) typically returned from a database query. Unlike a raw list of dicts,
a Record Set provides consistent operations: column access, filtering, and safe
iteration. It's a stable interface between a data-access layer and domain logic,
letting the domain stay ignorant of how data actually arrived (SQL, REST API, etc.).

In production, think of Record Set as what lives in memory after fetch; it's not
the query itself, but the result. It trades simplicity for power: no sorting,
no complex transformations. If you need those, move the logic to your Gateway.

This is a foundational pattern that pairs with Table Data Gateway (queries and
returns Record Sets) and Row Data Gateway (returns single rows, often wrapped
in Record Sets of 1).
"""
from typing import Any, Callable, Dict, List, Optional


class RecordSet:
    """An immutable in-memory collection of rows returned from a query.

    A Record Set is a thin wrapper around a list of dict rows, providing:
    - Column access (by name)
    - Safe iteration
    - Filtering by predicate
    - Defensive against modification (rows are dicts, but rows list is frozen)

    Rows are stored as dicts; the column names come from dict keys. This keeps
    the pattern simple and doesn't require upfront schema definition.

    Example:
        >>> rows = [
        ...     {"id": 1, "name": "Alice", "age": 30},
        ...     {"id": 2, "name": "Bob", "age": 25},
        ... ]
        >>> rs = RecordSet(rows)
        >>> rs.count()
        2
        >>> names = rs.column("name")
        >>> names
        ['Alice', 'Bob']
        >>> filtered = rs.where(lambda r: r["age"] > 26)
        >>> filtered.count()
        1
    """

    def __init__(self, rows: List[Dict[str, Any]]):
        """Initialize a Record Set with a list of rows.

        Args:
            rows: A list of dictionaries, each representing a row. Keys are
                column names, values are the cell data. Rows should have
                consistent keys, but this is not enforced.

        Raises:
            TypeError: If rows is not a list or contains non-dict entries.
        """
        if not isinstance(rows, list):
            raise TypeError("rows must be a list of dictionaries")
        if rows and not all(isinstance(r, dict) for r in rows):
            raise TypeError("all rows must be dictionaries")
        self._rows = list(rows)  # Defensive copy

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

        Args:
            name: The column name (dict key).

        Returns:
            A list of values for that column across all rows. If a row is
            missing the column, None is used in its place.

        Raises:
            ValueError: If the column name does not appear in any row.
        """
        if self.is_empty():
            raise ValueError(f"Cannot extract column '{name}' from empty Record Set")
        if not any(name in row for row in self._rows):
            raise ValueError(f"Column '{name}' not found in any row")
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
        """Filter rows by a predicate function.

        Args:
            predicate: A callable that takes a row dict and returns True if
                the row should be included.

        Returns:
            A new Record Set containing only the filtered rows.

        Example:
            >>> rs = RecordSet([{"id": 1, "age": 30}, {"id": 2, "age": 25}])
            >>> filtered = rs.where(lambda r: r["age"] > 26)
            >>> filtered.count()
            1
        """
        filtered = [r for r in self._rows if predicate(r)]
        return RecordSet(filtered)

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
