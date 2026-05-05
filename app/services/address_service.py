"""Service layer for address operations."""

import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate
from app.utils.geo import is_within_distance

logger = logging.getLogger(__name__)


def create_address(db: Session, payload: AddressCreate) -> Address:
    """Create and persist an address record."""
    try:
        address = Address(**payload.model_dump())
        db.add(address)
        db.commit()
        db.refresh(address)
        logger.info("Address created with id=%s", address.id)
        return address
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Failed to create address")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create address")


def list_addresses(db: Session) -> list[Address]:
    """Return all address records."""
    try:
        return db.query(Address).all()
    except SQLAlchemyError:
        logger.exception("Failed to fetch addresses")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to fetch addresses")


def get_address_by_id(db: Session, address_id: int) -> Address:
    """Return an address by id or raise 404."""
    try:
        address = db.query(Address).filter(Address.id == address_id).first()
    except SQLAlchemyError:
        logger.exception("Failed to fetch address id=%s", address_id)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to fetch address")

    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address with id={address_id} not found")
    return address


def update_address(db: Session, address_id: int, payload: AddressUpdate) -> Address:
    """Update an address with provided fields."""
    address = get_address_by_id(db, address_id)
    update_data = payload.model_dump(exclude_unset=True)

    try:
        for field_name, value in update_data.items():
            setattr(address, field_name, value)
        db.commit()
        db.refresh(address)
        logger.info("Address id=%s updated", address_id)
        return address
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Failed to update address id=%s", address_id)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to update address")


def delete_address(db: Session, address_id: int) -> None:
    """Delete an address by id."""
    address = get_address_by_id(db, address_id)
    try:
        db.delete(address)
        db.commit()
        logger.info("Address id=%s deleted", address_id)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Failed to delete address id=%s", address_id)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to delete address")


def find_nearby_addresses(
    db: Session,
    latitude: float,
    longitude: float,
    distance_km: float,
) -> list[Address]:
    """Return addresses within distance_km from the supplied origin point."""
    addresses = list_addresses(db)
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
