"""Tests for Data Transfer Object (DTO) pattern."""
import pytest
from dto import UserDTO, ProductDTO, DTOBase


class TestUserDTOCreation:
    """Tests for creating UserDTO instances."""

    def test_create_user_dto_with_all_fields(self):
        """Can create a UserDTO with all fields."""
        user = UserDTO(id=1, name="Alice", email="alice@example.com", is_active=True)
        assert user.id == 1
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert user.is_active is True

    def test_create_user_dto_with_default_is_active(self):
        """is_active field has a default value of True."""
        user = UserDTO(id=2, name="Bob", email="bob@example.com")
        assert user.is_active is True

    def test_user_dto_requires_id_name_email(self):
        """UserDTO requires id, name, and email fields."""
        with pytest.raises(TypeError):
            # Missing required fields
            UserDTO(id=1)


class TestProductDTOCreation:
    """Tests for creating ProductDTO instances."""

    def test_create_product_dto_with_required_fields_only(self):
        """Can create a ProductDTO with only required fields."""
        product = ProductDTO(id=1, name="Laptop", price_cents=99900)
        assert product.id == 1
        assert product.name == "Laptop"
        assert product.price_cents == 99900
        assert product.description is None
        assert product.stock_available is None

    def test_create_product_dto_with_all_fields(self):
        """Can create a ProductDTO with all fields including optional."""
        product = ProductDTO(
            id=1,
            name="Laptop",
            price_cents=99900,
            description="High-performance laptop",
            stock_available=5,
        )
        assert product.description == "High-performance laptop"
        assert product.stock_available == 5

    def test_product_dto_optional_fields_default_to_none(self):
        """Optional fields default to None if not provided."""
        product = ProductDTO(id=1, name="Mouse", price_cents=2500)
        assert product.description is None
        assert product.stock_available is None


class TestDTOImmutability:
    """Tests for DTO immutability (frozen dataclasses)."""

    def test_user_dto_is_immutable(self):
        """UserDTO cannot be modified after creation."""
        user = UserDTO(id=1, name="Alice", email="alice@example.com", is_active=True)

        # Attempting to modify should raise an error
        with pytest.raises(Exception):  # FrozenInstanceError
            user.name = "Bob"

    def test_product_dto_is_immutable(self):
        """ProductDTO cannot be modified after creation."""
        product = ProductDTO(id=1, name="Laptop", price_cents=99900)

        # Attempting to modify should raise an error
        with pytest.raises(Exception):  # FrozenInstanceError
            product.price_cents = 50000

    def test_dto_immutability_is_thread_safe(self):
        """Immutable DTOs can be safely shared across threads."""
        # This is a conceptual test - immutability makes thread safety trivial
        user = UserDTO(id=1, name="Alice", email="alice@example.com")

        # Multiple "threads" can read the same DTO without issues
        name1 = user.name
        name2 = user.name
        assert name1 == name2 == "Alice"


class TestDTOSerialization:
    """Tests for converting DTOs to/from dicts."""

    def test_user_dto_to_dict(self):
        """Can convert UserDTO to a dictionary."""
        user = UserDTO(id=1, name="Alice", email="alice@example.com", is_active=True)
        user_dict = user.to_dict()

        assert isinstance(user_dict, dict)
        assert user_dict["id"] == 1
        assert user_dict["name"] == "Alice"
        assert user_dict["email"] == "alice@example.com"
        assert user_dict["is_active"] is True

    def test_product_dto_to_dict_with_none_values(self):
        """to_dict() includes None values for optional fields."""
        product = ProductDTO(id=1, name="Mouse", price_cents=2500)
        product_dict = product.to_dict()

        assert product_dict["description"] is None
        assert product_dict["stock_available"] is None

    def test_user_dto_from_dict(self):
        """Can create UserDTO from a dictionary."""
        user_dict = {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "is_active": True,
        }
        user = UserDTO.from_dict(user_dict)

        assert user.id == 1
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert user.is_active is True

    def test_product_dto_from_dict_with_extra_fields(self):
        """from_dict() ignores extra fields not in the DTO."""
        product_dict = {
            "id": 1,
            "name": "Laptop",
            "price_cents": 99900,
            "description": "High-performance",
            "stock_available": 5,
            "extra_field": "should be ignored",
            "another_extra": 123,
        }
        product = ProductDTO.from_dict(product_dict)

        assert product.id == 1
        assert product.name == "Laptop"
        # Extra fields are simply ignored
        assert not hasattr(product, "extra_field")

    def test_round_trip_dto_to_dict_and_back(self):
        """Can convert DTO -> dict -> DTO with no data loss."""
        original_user = UserDTO(id=1, name="Alice", email="alice@example.com", is_active=True)
        user_dict = original_user.to_dict()
        reconstructed_user = UserDTO.from_dict(user_dict)

        # Should be identical
        assert reconstructed_user == original_user
        assert reconstructed_user.id == original_user.id
        assert reconstructed_user.name == original_user.name
        assert reconstructed_user.email == original_user.email
        assert reconstructed_user.is_active == original_user.is_active


class TestDTOEquality:
    """Tests for DTO equality comparison."""

    def test_dtos_with_same_fields_are_equal(self):
        """Two UserDTOs with identical fields are equal."""
        user1 = UserDTO(id=1, name="Alice", email="alice@example.com", is_active=True)
        user2 = UserDTO(id=1, name="Alice", email="alice@example.com", is_active=True)

        assert user1 == user2

    def test_dtos_with_different_fields_are_not_equal(self):
        """Two UserDTOs with different fields are not equal."""
        user1 = UserDTO(id=1, name="Alice", email="alice@example.com", is_active=True)
        user2 = UserDTO(id=2, name="Alice", email="alice@example.com", is_active=True)

        assert user1 != user2

    def test_dto_equality_is_based_on_values_not_identity(self):
        """DTOs are compared by value, not object identity."""
        user1 = UserDTO(id=1, name="Alice", email="alice@example.com")
        user2 = UserDTO(id=1, name="Alice", email="alice@example.com")

        # Different objects
        assert user1 is not user2
        # But equal values
        assert user1 == user2


class TestDTORepresentation:
    """Tests for DTO string representation."""

    def test_user_dto_has_readable_repr(self):
        """UserDTO has a readable string representation."""
        user = UserDTO(id=1, name="Alice", email="alice@example.com", is_active=True)
        repr_str = repr(user)

        # Should contain class name and field values
        assert "UserDTO" in repr_str
        assert "Alice" in repr_str
        assert "alice@example.com" in repr_str

    def test_product_dto_has_readable_repr(self):
        """ProductDTO has a readable string representation."""
        product = ProductDTO(id=1, name="Laptop", price_cents=99900)
        repr_str = repr(product)

        # Should contain class name and field values
        assert "ProductDTO" in repr_str
        assert "Laptop" in repr_str


class TestDTOBoundaryUsage:
    """Tests simulating real-world boundary usage."""

    def test_database_layer_to_api_layer_flow(self):
        """Simulates data flowing from database to API."""
        # STEP 1: Database returns a row as a dict
        db_row = {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "is_active": True,
        }

        # STEP 2: Convert to DTO at the boundary
        user_dto = UserDTO.from_dict(db_row)

        # STEP 3: API serializes DTO to dict (for JSON)
        api_response = user_dto.to_dict()

        # STEP 4: Verify data integrity
        assert api_response == db_row

    def test_api_request_to_domain_model_flow(self):
        """Simulates data flowing from API request to domain logic."""
        # STEP 1: Client sends JSON data (parsed into dict)
        request_data = {
            "name": "Bob",
            "email": "bob@example.com",
            "is_active": True,
        }

        # STEP 2: API adds server-generated ID
        request_data["id"] = 1

        # STEP 3: Convert request data to DTO
        user_dto = UserDTO.from_dict(request_data)

        # STEP 4: Domain logic can work with the DTO
        assert user_dto.id == 1
        assert user_dto.name == "Bob"

    def test_multiple_dto_formats_for_same_domain_object(self):
        """Different DTOs can represent the same object for different contexts."""
        # Public API might use one DTO format
        public_user = UserDTO(id=1, name="Alice", email="alice@example.com")

        # Internal service might use a different DTO with different fields
        internal_user = UserDTO(
            id=1,
            name="Alice",
            email="alice@example.com",
            is_active=True,
        )

        # Both represent the same user, just different views
        assert public_user.id == internal_user.id
