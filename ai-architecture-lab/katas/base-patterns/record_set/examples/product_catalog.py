"""Example: Querying a product catalog with Record Set.

SCENARIO:
We're building an e-commerce product catalog. A Table Data Gateway has fetched
product data from the database and returned a list of dict rows. We want to
work with these results safely without re-querying the database.

THIS EXAMPLE DEMONSTRATES:
1. Creating a Record Set from query results
2. Counting rows
3. Extracting a column (product names)
4. Filtering by single conditions
5. Chaining multiple filters
6. Iterating through filtered results

WHY RECORD SET IS USEFUL HERE:
- We can filter the results multiple ways without re-querying
- Each filter returns a NEW Record Set (immutable design)
- Column extraction is safe and returns copies
- Easy to test without a database
"""
import sys
from pathlib import Path

# Add parent directory to path so we can import RecordSet
sys.path.insert(0, str(Path(__file__).parent.parent))

from record_set import RecordSet


def main():
    """Run the product catalog example."""

    # STEP 1: Simulate rows returned by a Table Data Gateway query.
    # In a real app, these would come from a database query.
    # Each row is a dict with column names as keys.
    product_rows = [
        {"id": 1, "name": "Laptop", "price_cents": 99900, "in_stock": True},
        {"id": 2, "name": "Mouse", "price_cents": 2500, "in_stock": True},
        {"id": 3, "name": "Keyboard", "price_cents": 7500, "in_stock": False},
        {"id": 4, "name": "Monitor", "price_cents": 29900, "in_stock": True},
    ]

    # STEP 2: Wrap in Record Set for safe operations.
    # Record Set provides filtering, column extraction, and defensive copying.
    catalog = RecordSet(product_rows)

    print("=== Product Catalog ===\n")

    # OPERATION 1: Count total products in the catalog
    total_product_count = catalog.count()
    print(f"Total products: {total_product_count}")

    # OPERATION 2: Extract a single column (product names).
    # This is useful when you need all values for one column.
    # Example: building a dropdown list of product names
    product_names = catalog.column("name")
    print(f"\nAll product names: {product_names}")

    # OPERATION 3: Filter for in-stock items.
    # where() takes a predicate function (a lambda that returns True/False).
    # It returns a NEW Record Set with only matching rows.
    # The original catalog is unchanged (immutability).
    in_stock = catalog.where(lambda row: row["in_stock"])
    print(f"\nIn-stock products: {in_stock.count()}")
    for product in in_stock:
        # Convert price from cents to dollars for display
        product_name = product['name']
        price_in_dollars = product['price_cents'] / 100
        print(f"  - {product_name}: ${price_in_dollars:.2f}")

    # OPERATION 4: Filter for expensive items (more than $50).
    # Note: Prices are stored in cents (5000 cents = $50.00).
    # This separate filter doesn't affect the in_stock Record Set.
    expensive = catalog.where(lambda row: row["price_cents"] > 5000)
    print(f"\nExpensive products (>$50): {expensive.count()}")
    for product in expensive:
        # Get product details for display
        product_name = product['name']
        price_in_dollars = product["price_cents"] / 100
        is_in_stock = product["in_stock"]
        stock_status = "in stock" if is_in_stock else "out of stock"
        print(f"  - {product_name}: ${price_in_dollars:.2f} ({stock_status})")

    # OPERATION 5: Chain multiple filters together.
    # Find products that are BOTH in-stock AND expensive.
    # This shows how Record Set filtering is composable:
    # start with in_stock results, then filter those further.
    # This is much more efficient than querying the database twice.
    in_stock_expensive = in_stock.where(lambda row: row["price_cents"] > 5000)
    print(f"\nIn-stock AND expensive: {in_stock_expensive.count()}")
    for product in in_stock_expensive:
        product_name = product['name']
        price_in_dollars = product['price_cents'] / 100
        print(f"  - {product_name}: ${price_in_dollars:.2f}")

    # OPERATION 6: Get the first row from the catalog.
    # Useful for queries expected to return exactly one result,
    # or when you just need the "latest" item.
    first_product = catalog.first()
    if first_product:
        first_product_name = first_product['name']
        print(f"\nFirst product in catalog: {first_product_name}")

    print("\n=== Record Set Operations Complete ===")


if __name__ == "__main__":
    main()
