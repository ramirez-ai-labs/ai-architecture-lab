"""
Tests for Product Gateway Example.

Demonstrates extended gateway with domain-specific methods.
"""

import pytest
import sqlite3
import sys
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from examples.product_gateway import ProductGateway, create_product_table


@pytest.fixture
def db_connection():
    """Create an in-memory SQLite database for testing."""
    connection = sqlite3.connect(":memory:")
    create_product_table(connection)
    yield connection
    connection.close()


@pytest.fixture
def gateway(db_connection):
    """Create a ProductGateway for testing."""
    return ProductGateway(db_connection)


class TestProductGateway:
    """Test Product Gateway extended methods."""
    
    def test_find_by_name_finds_matching_products(self, gateway):
        """find_by_name() should find products by name."""
        gateway.insert({"name": "Widget", "price_cents": 1000, "stock_quantity": 50})
        gateway.insert({"name": "Gadget", "price_cents": 2000, "stock_quantity": 30})
        
        products = gateway.find_by_name("Widget")
        
        assert len(products) == 1
        assert products[0]["name"] == "Widget"
    
    def test_find_by_name_is_case_insensitive(self, gateway):
        """find_by_name() should be case-insensitive."""
        gateway.insert({"name": "Widget", "price_cents": 1000, "stock_quantity": 50})
        
        products_lower = gateway.find_by_name("widget")
        products_upper = gateway.find_by_name("WIDGET")
        
        assert len(products_lower) == 1
        assert len(products_upper) == 1
    
    def test_find_low_stock_finds_products_below_threshold(self, gateway):
        """find_low_stock() should find products with low stock."""
        gateway.insert({"name": "High Stock", "price_cents": 1000, "stock_quantity": 50})
        gateway.insert({"name": "Low Stock", "price_cents": 2000, "stock_quantity": 5})
        
        low_stock = gateway.find_low_stock(threshold=10)
        
        assert len(low_stock) == 1
        assert low_stock[0]["name"] == "Low Stock"
        assert low_stock[0]["stock_quantity"] == 5
    
    def test_find_low_stock_uses_default_threshold(self, gateway):
        """find_low_stock() should use default threshold of 10."""
        gateway.insert({"name": "High Stock", "price_cents": 1000, "stock_quantity": 50})
        gateway.insert({"name": "Low Stock", "price_cents": 2000, "stock_quantity": 5})
        gateway.insert({"name": "Medium Stock", "price_cents": 1500, "stock_quantity": 15})
        
        low_stock = gateway.find_low_stock()  # Default threshold = 10
        
        assert len(low_stock) == 1
        assert low_stock[0]["name"] == "Low Stock"
