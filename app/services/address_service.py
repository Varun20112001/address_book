from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate
from app.usecases.address_usecases import AddressUseCases


class AddressService:
    """Service facade used by API controllers."""

    def __init__(self, use_cases: AddressUseCases) -> None:
        self.use_cases = use_cases

    def create_address(self, payload: AddressCreate) -> Address:
        """Create and persist an address record."""
        return self.use_cases.create_address(payload)

    def list_addresses(self) -> list[Address]:
        """Return all address records."""
        return self.use_cases.list_addresses()

    def get_address_by_id(self, address_id: int) -> Address:
        """Return an address by id or raise 404."""
        return self.use_cases.get_address_by_id(address_id)

    def update_address(self, address_id: int, payload: AddressUpdate) -> Address:
        """Update an address with provided fields."""
        return self.use_cases.update_address(address_id, payload)

    def delete_address(self, address_id: int) -> None:
        """Delete an address by id."""
        self.use_cases.delete_address(address_id)

    def find_nearby_addresses(self, latitude: float, longitude: float, distance_km: float) -> list[Address]:
        """Return addresses within distance_km from the supplied origin point."""
        return self.use_cases.find_nearby_addresses(latitude, longitude, distance_km)
