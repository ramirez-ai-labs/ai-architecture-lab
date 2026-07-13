# Record Set Pattern

An in-memory tabular representation of query results, providing a stable interface for working with rows without re-querying the database.

---

## 🌱 What Is Record Set?

**Record Set** is a lightweight wrapper around a list of rows (dictionaries) that provides a consistent, predictable interface for:

- Accessing rows by index or iterating through them
- Extracting entire columns by name
- Filtering rows by predicates
- Defensive copying to prevent accidental mutations

A Record Set is not a query engine; it's the *result* of a query wrapped in a safe container. Think of it as what lives in memory *after* your Table Data Gateway has fetched rows from the database.

### Key Characteristics

- ✅ **Immutable rows list** — once created, the Record Set's row collection doesn't change
- ✅ **Safe column extraction** — get all values for a column across rows
- ✅ **Chainable filtering** — filter rows and get another Record Set
- ✅ **Iterable** — loop through rows naturally
- ✅ **No schema definition** — rows are plain dicts; columns come from keys
- ✅ **Defensive copies** — getters return copies to prevent external modification

---

## 🎓 Why Use Record Set?

### Benefits

1. **Clear contract at data-access boundary**: Table Data Gateway returns Record Set; domain code expects Record Set. No surprises.
2. **Prevents accidental mutation**: If you get a row from Record Set, you're getting a copy. Modifying it doesn't break the Record Set.
3. **Simple to test**: Create a Record Set with test data, no DB needed. Easy to unit test filtering logic.
4. **Chainable filtering**: Filter once, then filter again. Each step returns a new Record Set.
5. **Consistent operations**: Whether a Record Set came from a query or from a test, the interface is identical.

### When to Use

- ✅ After fetching rows from a database or API
- ✅ When you need to provide a stable interface to domain logic
- ✅ When filtering/transforming happens in memory (not at the DB level)
- ✅ When you want defensive copying without heavy lifting

### When NOT to Use

- ❌ When you need sorting or complex transformations (push that to the database query or use a DataFrame library)
- ❌ For massive datasets where copying every row is prohibitively expensive (use a cursor/lazy iterator instead)
- ❌ When the schema is highly dynamic or schema-less (consider a document store pattern)
- ❌ When you need aggregate operations like SUM or COUNT (use SQL or a dedicated analytics library)

---

## 📁 Structure

```
record_set/
├── record_set.py              # RecordSet implementation
├── examples/
│   └── product_catalog.py     # Example: querying a product catalog
├── tests/
│   └── test_record_set.py     # 18 comprehensive tests
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ai-architecture-lab/katas/base-patterns/record_set
pip install -r requirements.txt
```

### 2. Run Tests

```bash
# Run all tests (recommended)
pytest -v

# Run specific test class
pytest tests/test_record_set.py::TestRecordSetFiltering -v
```

### 3. Explore the Code

Start with:
1. `record_set.py` — RecordSet class implementation (60 lines, very readable)
2. `examples/product_catalog.py` — Real-world catalog query example
3. `tests/test_record_set.py` — Comprehensive test suite showing all patterns

---

## 💡 Usage Examples

### Creating a Record Set

```python
from record_set import RecordSet

# Simulate rows returned by a Table Data Gateway query
rows = [
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 25},
    {"id": 3, "name": "Charlie", "age": 35},
]

rs = RecordSet(rows)
```

### Basic Operations

```python
# Get row count
print(rs.count())  # 3

# Get first row
first = rs.first()  # {"id": 1, "name": "Alice", "age": 30}

# Get row by index
row = rs.row(0)

# Get all rows as list
all_rows = rs.rows()

# Check if empty
if not rs.is_empty():
    print("Record Set has data")
```

### Column Extraction

```python
# Extract a single column across all rows
names = rs.column("name")  # ["Alice", "Bob", "Charlie"]

# Extract numeric column
ages = rs.column("age")    # [30, 25, 35]
```

### Filtering with Predicates

```python
# Filter for adults over 26
adults = rs.where(lambda r: r["age"] > 26)
print(adults.count())  # 2

# Chain filters: age > 26 AND name starts with C
filtered = (rs
    .where(lambda r: r["age"] > 26)
    .where(lambda r: r["name"].startswith("C")))
print(filtered.count())  # 1
```

### Iteration

```python
# Iterate naturally
for row in rs:
    print(f"{row['name']}: {row['age']}")

# Build a domain object from each row
from dataclasses import dataclass

@dataclass
class Person:
    id: int
    name: str
    age: int

people = [Person(**row) for row in rs]
```

---

## 🧪 Test Coverage

This kata includes 18 comprehensive tests organized into 6 test classes:

**Initialization Tests (5)**
- Empty Record Set creation
- Record Set with rows
- Type validation (rejects non-list, non-dict rows)
- Defensive copy on input

**Basic Operations (7)**
- Count, is_empty, row access by index
- Out-of-bounds handling
- Row copies prevent external modification
- First row access, all rows as list

**Column Extraction (4)**
- Extract existing column
- Error on non-existent column
- Error on empty Record Set
- Handling missing keys in some rows (returns None)

**Filtering Tests (6)**
- Filter by predicate
- Chained filters
- No matches, all match scenarios
- String column matching

**Iteration Tests (2)**
- Natural iteration over rows
- Iteration yields copies

**Edge Cases (4)**
- Heterogeneous rows (different column sets)
- Empty dicts as rows
- String representation

Run tests to see all patterns in action:

```bash
pytest tests/test_record_set.py -v
```

---

## 🔗 Related Patterns

- **Table Data Gateway** (`../table_data_gateway/`) — Fetches rows from database, returns Record Set
- **Row Data Gateway** — Returns single rows; often wrapped in a Record Set of 1
- **Active Record** — Alternative: entities that know how to fetch and save themselves
- **Data Mapper** — Maps database rows to domain objects; Record Set is often an intermediate step
- **Entity** — Domain objects with identity; Record Set contains plain dicts, not entities

---

## 📚 Learning Path

1. **Start here**: Understand Record Set as a simple tabular container
2. **Try filtering**: Experiment with predicates and chaining
3. **Explore iteration**: See how to transform rows into domain objects
4. **Study column access**: Understand defensive copying and missing keys
5. **Next kata**: Move to Table Data Gateway (returns Record Sets from queries)

---

## 🎯 Key Takeaways

1. **Record Set is a result wrapper** — not a query tool, but a safe container for query results
2. **Operations return new Record Sets** — filtering doesn't mutate the original; you chain safely
3. **Defensive copying prevents bugs** — rows from Record Set are copies, not references
4. **Plain dicts, no schema** — rows are dicts; column names come from keys
5. **Pairs with Table Data Gateway** — one fetches, the other holds the results safely

---

## 📝 Notes

- **Columns with missing keys**: If a row lacks a key, `column()` returns `None` for that row
- **Iteration yields copies**: Modifying a row during iteration doesn't affect the Record Set
- **Empty Record Sets**: Most operations on empty Record Sets are safe; some (like `column()`) raise ValueError
- **Performance**: For massive datasets (millions of rows), consider lazy evaluation or cursors instead
- **Schema flexibility**: Record Set doesn't enforce a schema; rows can have different columns

---

## ⚠️ Important: When NOT to Use Record Set

Record Set is powerful but simple. If you find yourself:

- Sorting rows (push to database with `ORDER BY`)
- Aggregating (use `SUM`, `COUNT` in SQL)
- Joining multiple Record Sets (consider a real query or a dedicated join function)
- Working with streaming data (use an iterator or cursor)

...then Record Set isn't the right tool. Stick with SQL queries, DataFrames, or other patterns designed for those use cases.

---

**Next Steps:** After understanding Record Set, move to the `Table Data Gateway` kata to see how queries return Record Sets, or explore `Data Mapper` to see how Record Sets become domain objects.
