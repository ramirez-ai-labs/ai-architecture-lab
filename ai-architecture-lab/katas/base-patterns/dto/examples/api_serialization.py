"""Example: Serializing DTOs for API responses.

SCENARIO:
We're building a REST API that returns user and product data.
DTOs are perfect for this because they:
- Serialize easily to JSON
- Hide internal implementation details
- Provide a stable API contract

THIS EXAMPLE DEMONSTRATES:
1. Creating DTOs from database-like data
2. Converting DTOs to JSON-serializable dicts
3. Creating DTOs from API requests
4. Building API responses with DTOs
"""
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dto import UserDTO, ProductDTO


def main():
    """Run the API serialization example."""

    print("=== Data Transfer Objects for API Responses ===\n")

    # =========================================================================
    # OPERATION 1: Simulate database query results
    # =========================================================================
    print("--- OPERATION 1: Database Query Results ---\n")

    # Simulated database rows (raw dicts from SELECT query)
    user_rows_from_db = [
        {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "is_active": True},
        {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "is_active": True},
        {"id": 3, "name": "Charlie Brown", "email": "charlie@example.com", "is_active": False},
    ]

    product_rows_from_db = [
        {"id": 101, "name": "Laptop", "price_cents": 99900, "description": "High-performance laptop", "stock_available": 5},
        {"id": 102, "name": "Mouse", "price_cents": 2500, "description": None, "stock_available": 50},
        {"id": 103, "name": "Keyboard", "price_cents": 7500, "description": "Mechanical keyboard", "stock_available": None},
    ]

    print(f"Database returned {len(user_rows_from_db)} user rows")
    print(f"Database returned {len(product_rows_from_db)} product rows\n")

    # =========================================================================
    # OPERATION 2: Convert database rows to DTOs
    # =========================================================================
    print("--- OPERATION 2: Convert to DTOs ---\n")

    # Create DTOs from database rows
    # This is the boundary between "database layer" and "API layer"
    users = [UserDTO.from_dict(row) for row in user_rows_from_db]
    products = [ProductDTO.from_dict(row) for row in product_rows_from_db]

    print(f"Created {len(users)} UserDTOs from database rows")
    print(f"Created {len(products)} ProductDTOs from database rows")
    print(f"\nFirst user DTO: {users[0]}\n")

    # =========================================================================
    # OPERATION 3: Serialize DTOs to JSON for API response
    # =========================================================================
    print("--- OPERATION 3: Serialize to JSON ---\n")

    # Build API response with DTOs
    # In a real API framework (Flask, FastAPI), this would be automatic
    api_response = {
        "status": "success",
        "data": {
            "users": [user.to_dict() for user in users],
            "products": [product.to_dict() for product in products],
        },
        "count": {
            "users": len(users),
            "products": len(products),
        },
    }

    # Convert to JSON (what the API actually sends to client)
    json_response = json.dumps(api_response, indent=2)
    print("API Response (JSON):")
    print(json_response[:500] + "...\n")  # Show first 500 chars

    # =========================================================================
    # OPERATION 4: Simulate receiving API request data
    # =========================================================================
    print("--- OPERATION 4: Deserialize from API Request ---\n")

    # Simulate client sending JSON data to create a new user
    client_request_json = {
        "name": "Diana Prince",
        "email": "diana@example.com",
        "is_active": True,
    }

    print(f"Received API request: {client_request_json}")

    # Add an ID (server would generate this)
    client_request_json["id"] = 4

    # Create DTO from the client request
    new_user_dto = UserDTO.from_dict(client_request_json)
    print(f"Created DTO from request: {new_user_dto}\n")

    # =========================================================================
    # OPERATION 5: Show DTO immutability
    # =========================================================================
    print("--- OPERATION 5: DTO Immutability ---\n")

    # DTOs are immutable (frozen=True)
    # This means you can't modify them after creation
    print(f"Original user: {users[0]}")
    print("Attempting to modify user.name...")

    try:
        # This will raise an error because DTOs are immutable
        users[0].name = "Alice Modified"
        print("ERROR: Should not be able to modify!")
    except Exception as error:
        print(f"✓ Correctly prevented modification: {type(error).__name__}")
        print(f"  Message: {error}\n")

    # =========================================================================
    # OPERATION 6: Show safe field access
    # =========================================================================
    print("--- OPERATION 6: Safe Field Access ---\n")

    # DTOs provide a predictable interface
    # You know exactly what fields are available
    product = products[0]
    print(f"Product ID: {product.id}")
    print(f"Product Name: {product.name}")
    print(f"Product Price: ${product.price_cents / 100:.2f}")
    print(f"Product Description: {product.description}")
    print(f"Product Stock: {product.stock_available}")

    print("\n=== Data Transfer Objects Example Complete ===")


if __name__ == "__main__":
    main()
