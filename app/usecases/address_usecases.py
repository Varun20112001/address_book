"""Address application use cases."""

import logging

from fastapi import HTTPException, status

from app.models.address import Address
from app.repositories.address_repository import AbstractAddressRepository, AddressRepositoryError
from app.schemas.address import AddressCreate, AddressUpdate
from app.utils.geo import is_within_distance

logger = logging.getLogger(__name__)


class AddressUseCases:
    """Business use cases for address operations."""

    def __init__(self, repository: AbstractAddressRepository) -> None:
        self.repository = repository

    def create_address(self, payload: AddressCreate) -> Address:
        """Create and persist an address record."""
        try:
            return self.repository.create(payload)
        except AddressRepositoryError as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

    def list_addresses(self) -> list[Address]:
        """Return all address records."""
        try:
            return self.repository.list()
        except AddressRepositoryError as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

    def get_address_by_id(self, address_id: int) -> Address:
        """Return an address by id or raise 404."""
        try:
            address = self.repository.get_by_id(address_id)
        except AddressRepositoryError as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

        if address is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address with id={address_id} not found")
        return address

    def update_address(self, address_id: int, payload: AddressUpdate) -> Address:
        """Update an address with provided fields."""
        address = self.get_address_by_id(address_id)
        update_data = payload.model_dump(exclude_unset=True)

        try:
            return self.repository.update(address, update_data)
        except AddressRepositoryError as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

    def delete_address(self, address_id: int) -> None:
        """Delete an address by id."""
        address = self.get_address_by_id(address_id)
        try:
            self.repository.delete(address)
        except AddressRepositoryError as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

    def find_nearby_addresses(self, latitude: float, longitude: float, distance_km: float) -> list[Address]:
        """Return addresses within distance_km from the supplied origin point."""
        addresses = self.list_addresses()
        nearby = [
            address
            for address in addresses
            if is_within_distance(latitude, longitude, address.latitude, address.longitude, distance_km)
        ]
        logger.info(
            "Found %s addresses within %skm of (%s, %s)",
            len(nearby),
            distance_km,
            latitude,
            longitude,
        )
        return nearby
