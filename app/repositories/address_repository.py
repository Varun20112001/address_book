"""Repository layer for address persistence."""

from abc import ABC, abstractmethod
import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.address import Address
from app.schemas.address import AddressCreate

logger = logging.getLogger(__name__)


class AddressRepositoryError(Exception):
    """Raised when address persistence operations fail."""


class AbstractAddressRepository(ABC):
    """Interface for address persistence operations."""

    @abstractmethod
    def create(self, payload: AddressCreate) -> Address:
        """Create and persist an address record."""

    @abstractmethod
    def list(self) -> list[Address]:
        """Return all address records."""

    @abstractmethod
    def get_by_id(self, address_id: int) -> Address | None:
        """Return an address by id when it exists."""

    @abstractmethod
    def update(self, address: Address, update_data: dict[str, object]) -> Address:
        """Persist updates to an existing address."""

    @abstractmethod
    def delete(self, address: Address) -> None:
        """Delete an address record."""


class SqlAlchemyAddressRepository(AbstractAddressRepository):
    """SQLAlchemy implementation of the address repository."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, payload: AddressCreate) -> Address:
        try:
            address = Address(**payload.model_dump())
            self.db.add(address)
            self.db.commit()
            self.db.refresh(address)
            logger.info("Address created with id=%s", address.id)
            return address
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.exception("Failed to create address")
            raise AddressRepositoryError("Unable to create address") from exc

    def list(self) -> list[Address]:
        try:
            return self.db.query(Address).all()
        except SQLAlchemyError as exc:
            logger.exception("Failed to fetch addresses")
            raise AddressRepositoryError("Unable to fetch addresses") from exc

    def get_by_id(self, address_id: int) -> Address | None:
        try:
            return self.db.query(Address).filter(Address.id == address_id).first()
        except SQLAlchemyError as exc:
            logger.exception("Failed to fetch address id=%s", address_id)
            raise AddressRepositoryError("Unable to fetch address") from exc

    def update(self, address: Address, update_data: dict[str, object]) -> Address:
        try:
            for field_name, value in update_data.items():
                setattr(address, field_name, value)
            self.db.commit()
            self.db.refresh(address)
            logger.info("Address id=%s updated", address.id)
            return address
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.exception("Failed to update address id=%s", address.id)
            raise AddressRepositoryError("Unable to update address") from exc

    def delete(self, address: Address) -> None:
        try:
            address_id = address.id
            self.db.delete(address)
            self.db.commit()
            logger.info("Address id=%s deleted", address_id)
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.exception("Failed to delete address id=%s", address.id)
            raise AddressRepositoryError("Unable to delete address") from exc
