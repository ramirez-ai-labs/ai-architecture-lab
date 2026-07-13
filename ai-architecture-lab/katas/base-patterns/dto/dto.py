"""Data Transfer Objects (DTOs) for moving data across system boundaries.

WHAT IS A DATA TRANSFER OBJECT?
A Data Transfer Object (DTO) is a simple object designed to transfer data
between different parts of a system or across network boundaries.

KEY CHARACTERISTIC: DTOs have NO BEHAVIOR.
A DTO is just data + structure. No business logic, no methods that do anything
except store and retrieve values. This makes them:
- Easy to serialize (convert to JSON, XML, etc.)
- Language-agnostic (can be used in different languages)
- Fast (no overhead of complex objects)
- Predictable (always contain the same fields)

DTO vs DOMAIN MODEL:
Domain Model (Entity): Rich behavior, business rules, validation
    account = Account(customer_id=123)
    account.deposit(amount)  # Has behavior
    account.validate()        # Has business logic

DTO: Just data, no behavior
    user_dto = UserDTO(id=123, name="Alice", email="alice@example.com")
    # No methods except getters/setters

WHEN TO USE EACH:
- Domain Model: Inside your service (business logic, complex state)
- DTO: At boundaries (APIs, databases, external services)

EXAMPLE FLOW:
1. Database returns rows (dicts)
2. Map rows to DTOs for transport
3. API returns DTOs (serialized to JSON)
4. Client receives JSON
5. Client parses JSON into DTOs
6. Client's domain logic uses DTOs

This pattern keeps layers independent. Database schema changes don't affect
the API contract if you manage the mapping correctly.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DTOBase:
    """Base class for all DTOs.

    WHY FROZEN=TRUE?
    frozen=True makes the dataclass immutable. Once created, a DTO cannot be changed.
    This is important because:
    - DTOs cross boundaries (network, processes, threads)
    - Immutability prevents accidental modifications
    - Immutable objects are thread-safe
    - Easier to reason about (no hidden state changes)

    WHAT IS A DATACLASS?
    A dataclass automatically generates __init__, __repr__, __eq__, and other
    methods based on the field annotations. This saves boilerplate code.
    """

    def to_dict(self) -> dict:
        """Convert DTO to a dictionary.

        WHAT DOES THIS DO?
        Converts the DTO to a plain dict. Useful for:
        - Serialization (convert to JSON)
        - Logging (dict is easier to print than object)
        - Testing (compare dicts instead of objects)

        Returns:
            A dictionary with all fields from this DTO.
        """
        # Import at runtime to avoid circular imports
        from dataclasses import asdict
        # Convert all dataclass fields to a dict
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "DTOBase":
        """Create a DTO from a dictionary.

        WHAT DOES THIS DO?
        Converts a plain dict back into a DTO. Useful for:
        - Deserialization (convert from JSON)
        - Reading from database rows (dicts)
        - Reconstructing objects from API responses

        Args:
            data: A dictionary with keys matching DTO field names.

        Returns:
            A new instance of this DTO class populated with values from data.

        Raises:
            TypeError: If data is missing required fields.
        """
        # Create a new instance using field names from the dict
        # Only pass fields that exist in this class
        field_names = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered_data)


@dataclass(frozen=True)
class UserDTO(DTOBase):
    """A Data Transfer Object representing a user.

    WHAT FIELDS DOES A USER DTO HAVE?
    This DTO is designed to transfer user data across system boundaries.
    It contains only data, no behavior.

    FIELDS:
    - id: Unique user identifier
    - name: User's display name
    - email: User's email address
    - is_active: Whether the user account is enabled

    WHY THESE FIELDS?
    These fields are:
    - Commonly needed across system boundaries
    - Safe to expose in APIs (no sensitive data)
    - Sufficient for most use cases (queries, display, etc.)

    EXAMPLE USAGE:
        # Create from scratch
        user_dto = UserDTO(id=1, name="Alice", email="alice@example.com", is_active=True)

        # Create from database row
        row = {"id": 1, "name": "Alice", "email": "alice@example.com", "is_active": True}
        user_dto = UserDTO.from_dict(row)

        # Serialize for API response
        response = user_dto.to_dict()  # Returns dict, convert to JSON

        # Access fields (immutable)
        print(user_dto.name)  # "Alice"
        # user_dto.name = "Bob"  # ERROR: Cannot modify (frozen=True)
    """

    id: int
    name: str
    email: str
    is_active: bool = True


@dataclass(frozen=True)
class ProductDTO(DTOBase):
    """A Data Transfer Object representing a product.

    WHAT FIELDS DOES A PRODUCT DTO HAVE?
    This DTO is designed to transfer product data across system boundaries.
    Contains only data relevant to displaying/querying products.

    FIELDS:
    - id: Unique product identifier
    - name: Product display name
    - price_cents: Price in cents (not dollars, to avoid float precision issues)
    - description: Product description (optional)
    - stock_available: Number of units in stock (optional)

    WHY OPTIONAL FIELDS?
    Some fields (description, stock_available) are optional because:
    - They may not be available in all contexts
    - Different APIs might need different fields
    - Flexibility in what data you expose

    EXAMPLE USAGE:
        # Create with required fields only
        product_dto = ProductDTO(id=1, name="Laptop", price_cents=99900)

        # Create with all fields
        product_dto = ProductDTO(
            id=1,
            name="Laptop",
            price_cents=99900,
            description="High-performance laptop",
            stock_available=5
        )

        # Create from database row
        row = {"id": 1, "name": "Laptop", "price_cents": 99900}
        product_dto = ProductDTO.from_dict(row)

        # Serialize for API response
        response = product_dto.to_dict()
    """

    id: int
    name: str
    price_cents: int
    description: Optional[str] = None
    stock_available: Optional[int] = None
