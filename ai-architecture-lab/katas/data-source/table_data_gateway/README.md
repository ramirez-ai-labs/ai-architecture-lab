# Table Data Gateway Pattern Kata

A hands-on demonstration of the **Table Data Gateway** pattern from PoEAA (Patterns of Enterprise Application Architecture).

---

## 🌱 What Is a Table Data Gateway?

A **Table Data Gateway** is an object that encapsulates all access to a database table. It acts as a gateway between your application code and the database.

### Key Characteristics

- ✅ **One gateway per table**: Each table has its own gateway object
- ✅ **Encapsulates SQL**: All SQL queries live in the gateway
- ✅ **Returns simple data**: Returns dictionaries or simple objects (not domain objects)
- ✅ **Hides database details**: Application code doesn't see SQL or connection management
- ✅ **Table-level operations**: Provides CRUD operations at the table level

### Why Use Table Data Gateway?

- **Separation of concerns**: Database access separate from business logic
- **Easier testing**: Can mock gateway instead of database
- **Reduces duplication**: SQL queries in one place
- **Simplifies changes**: Change database structure in gateway, not everywhere
- **Clear interface**: Simple CRUD methods (find_all, find_by_id, insert, update, delete)

---

## 🎓 When to Use Table Data Gateway?

### ✅ Good For:

- Simple applications with straightforward data access
- When you need table-level operations (not row-level)
- When you want to hide SQL from business logic
- When you need a simple, clear data access layer
- Applications where data structure matches table structure

### ❌ Not Good For:

- Complex domain models (use Repository or Data Mapper instead)
- When you need rich domain objects (gateway returns simple dicts)
- Complex queries with joins (consider Repository pattern)
- When you need transaction management across multiple tables

---

## 📁 Structure

```
table_data_gateway/
├── table_data_gateway.py    # Base TableDataGateway class
├── examples/
│   └── product_gateway.py   # Product gateway example
├── tests/
│   ├── test_table_data_gateway.py  # Tests for base class
│   └── test_product_gateway.py     # Tests for Product gateway
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ai-architecture-lab/katas/data-source/table_data_gateway
pip install -r requirements.txt
```

### 2. Run Tests

```bash
# Run all tests (recommended)
pytest -v

# Run specific test file
pytest tests/test_table_data_gateway.py -v
```

### 3. Explore the Code

Start with:
1. `table_data_gateway.py` - Base gateway class
2. `examples/product_gateway.py` - Product gateway example
3. `tests/` - Comprehensive test suite

---

## 💡 Usage Examples

### Basic CRUD Operations

```python
import sqlite3
from table_data_gateway import TableDataGateway

# Create in-memory database
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price_cents INTEGER NOT NULL
    )
""")
connection.commit()

# Create gateway
gateway = TableDataGateway(connection, "products")

# Insert
product_id = gateway.insert({
    "name": "Widget",
    "price_cents": 1000
})

# Find by ID
product = gateway.find_by_id(product_id)
print(product)  # {'id': 1, 'name': 'Widget', 'price_cents': 1000}

# Find all
all_products = gateway.find_all()
print(len(all_products))  # 1

# Update
gateway.update(product_id, {"price_cents": 1500})

# Delete
gateway.delete(product_id)

connection.close()
```

### Extended Gateway (Product Example)

```python
from examples.product_gateway import ProductGateway, create_product_table
import sqlite3

# Create database and table
connection = sqlite3.connect(":memory:")
create_product_table(connection)

# Create gateway
gateway = ProductGateway(connection)

# Insert products
gateway.insert({
    "name": "Widget",
    "price_cents": 1000,
    "stock_quantity": 50
})

# Use extended methods
low_stock = gateway.find_low_stock(threshold=10)
products = gateway.find_by_name("Widget")

connection.close()
```

---

## 🧪 Test Coverage

This kata includes comprehensive tests demonstrating:

- ✅ Gateway creation and initialization
- ✅ Insert operations (create)
- ✅ Find operations (read)
- ✅ Update operations
- ✅ Delete operations
- ✅ Count operations
- ✅ Error handling
- ✅ Extended gateway methods

Run tests to see all examples in action:

```bash
pytest -v
```

---

## 🔗 Related Patterns

- **Row Data Gateway**: Row-level operations (see `../row_data_gateway/`)
- **Active Record**: Entities that persist themselves
- **Data Mapper**: Maps between domain objects and database
- **Repository**: More sophisticated data access pattern

---

## 📚 Learning Path

1. **Start here**: Understand the base `TableDataGateway` class
2. **Study CRUD**: See how find_all, find_by_id, insert, update, delete work
3. **Try extended gateway**: See `ProductGateway` for domain-specific methods
4. **Run tests**: Understand behavior through test cases
5. **Next kata**: Move to `Row Data Gateway` (row-level operations)

---

## 🎯 Key Takeaways

1. **One gateway per table** - Each table has its own gateway
2. **Encapsulates SQL** - All database queries in one place
3. **Returns simple data** - Dictionaries, not domain objects
4. **Hides database details** - Application code doesn't see SQL
5. **Easy to test** - Can mock gateway instead of database

---

## 💻 Creating Your Own Gateway

To create a new gateway:

1. **Extend `TableDataGateway`**:
```python
from table_data_gateway import TableDataGateway

class MyTableGateway(TableDataGateway):
    def __init__(self, connection):
        super().__init__(connection, "my_table")
    
    def find_by_custom_field(self, value):
        """Custom find method."""
        query = "SELECT * FROM my_table WHERE custom_field = ?"
        # ... implementation
```

2. **Add domain-specific methods** (optional):
```python
def find_by_status(self, status: str):
    """Find rows by status."""
    # Custom query logic
```

3. **Write tests**:
```python
def test_custom_method():
    gateway = MyTableGateway(connection)
    results = gateway.find_by_custom_field("value")
    assert len(results) > 0
```

---

## 📝 Notes

- **SQLite**: This kata uses SQLite (built-in, no external DB needed)
- **In-memory testing**: Tests use `:memory:` database for isolation
- **Simple data structures**: Returns dicts, not domain objects
- **Transaction handling**: Basic commit after operations
- **Error handling**: Validates inputs and handles missing rows

---

## ⚠️ Important: Gateway vs Repository

**Table Data Gateway:**
- Returns simple data (dicts, tuples)
- Table-level operations
- Good for simple applications

**Repository:**
- Returns domain objects
- More sophisticated queries
- Better for complex domain models

Choose based on your application's complexity!

---

**Next Steps:** After understanding Table Data Gateway, move to `Row Data Gateway` which provides row-level operations, or `Active Record` for entities that persist themselves.
