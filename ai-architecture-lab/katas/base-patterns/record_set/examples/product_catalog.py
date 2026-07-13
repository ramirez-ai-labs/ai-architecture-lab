"""Example: Querying a product catalog with Record Set.

Simulates a Table Data Gateway that returns product rows, then uses Record Set
to work with the results safely without re-querying.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from record_set import RecordSet


def main():
    # Simulate rows returned by a Table Data Gateway query
    product_rows = [
        {"id": 1, "name": "Laptop", "price_cents": 99900, "in_stock": True},
        {"id": 2, "name": "Mouse", "price_cents": 2500, "in_stock": True},
        {"id": 3, "name": "Keyboard", "price_cents": 7500, "in_stock": False},
        {"id": 4, "name": "Monitor", "price_cents": 29900, "in_stock": True},
    ]

    # Wrap in Record Set for safe operations
    catalog = RecordSet(product_rows)

    print("=== Product Catalog ===\n")
    print(f"Total products: {catalog.count()}")

    # Extract a column
    product_names = catalog.column("name")
    print(f"\nAll product names: {product_names}")

    # Filter for in-stock items
    in_stock = catalog.where(lambda r: r["in_stock"])
    print(f"\nIn-stock products: {in_stock.count()}")
    for product in in_stock:
        print(f"  - {product['name']}: ${product['price_cents'] / 100:.2f}")

    # Filter for expensive items (> $50)
    expensive = catalog.where(lambda r: r["price_cents"] > 5000)
    print(f"\nExpensive products (>$50): {expensive.count()}")
    for product in expensive:
        price_dollars = product["price_cents"] / 100
        status = "in stock" if product["in_stock"] else "out of stock"
        print(f"  - {product['name']}: ${price_dollars:.2f} ({status})")

    # Chain filters: in stock AND expensive
    in_stock_expensive = in_stock.where(lambda r: r["price_cents"] > 5000)
    print(f"\nIn-stock AND expensive: {in_stock_expensive.count()}")
    for product in in_stock_expensive:
        print(f"  - {product['name']}: ${product['price_cents'] / 100:.2f}")

    # Get the first result
    first_product = catalog.first()
    if first_product:
        print(f"\nFirst product in catalog: {first_product['name']}")

    print("\n=== Record Set Operations Complete ===")


if __name__ == "__main__":
    main()
