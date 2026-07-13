"""
Product Gateway Example

Demonstrates Table Data Gateway pattern with a Product table.
"""

import sqlite3
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from table_data_gateway.table_data_gateway import TableDataGateway


def create_product_table(connection: sqlite3.Connection):
    """
    Create the products table for demonstration.
    
    Args:
        connection: SQLite database connection
    """
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price_cents INTEGER NOT NULL,
            stock_quantity INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    cursor.close()


class ProductGateway(TableDataGateway):
    """
    Gateway for the products table.
    
    Extends TableDataGateway with product-specific methods.
    """
    
    def __init__(self, connection: sqlite3.Connection):
        """Initialize Product Gateway."""
        super().__init__(connection, "products")
    
    def find_by_name(self, name: str):
        """
        Find products by name (case-insensitive).
        
        Args:
            name: Product name to search for
            
        Returns:
            List of product dictionaries matching the name
        """
        query = "SELECT * FROM products WHERE LOWER(name) = LOWER(?)"
        cursor = self._connection.cursor()
        cursor.execute(query, (name,))
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        # Convert rows to dictionaries
        rows = []
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            rows.append(row_dict)
        
        cursor.close()
        return rows
    
    def find_low_stock(self, threshold: int = 10):
        """
        Find products with stock below threshold.
        
        Args:
            threshold: Stock quantity threshold
            
        Returns:
            List of product dictionaries with low stock
        """
        query = "SELECT * FROM products WHERE stock_quantity < ?"
        cursor = self._connection.cursor()
        cursor.execute(query, (threshold,))
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        # Convert rows to dictionaries
        rows = []
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            rows.append(row_dict)
        
        cursor.close()
        return rows


# Example usage
if __name__ == "__main__":
    # Create in-memory database
    connection = sqlite3.connect(":memory:")
    create_product_table(connection)
    
    # Create gateway
    gateway = ProductGateway(connection)
    
    # Insert products
    product1_id = gateway.insert({
        "name": "Widget",
        "price_cents": 1000,  # $10.00
        "stock_quantity": 50
    })
    
    product2_id = gateway.insert({
        "name": "Gadget",
        "price_cents": 2500,  # $25.00
        "stock_quantity": 5
    })
    
    # Find all products
    all_products = gateway.find_all()
    print(f"Total products: {len(all_products)}")
    
    # Find by ID
    product = gateway.find_by_id(product1_id)
    print(f"Product 1: {product['name']} - ${product['price_cents'] / 100:.2f}")
    
    # Find low stock
    low_stock = gateway.find_low_stock(threshold=10)
    print(f"Low stock products: {len(low_stock)}")
    
    # Update product
    gateway.update(product1_id, {"stock_quantity": 100})
    
    # Delete product
    gateway.delete(product2_id)
    
    connection.close()
