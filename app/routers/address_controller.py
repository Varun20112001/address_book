"""Router module for address-related API endpoints."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.schemas.address import AddressCreate, AddressResponse, AddressUpdate
from address_book.app.services.address_service import (
    create_address,
    delete_address,
    find_nearby_addresses,
    get_address_by_id,
    list_addresses,
    update_address,
)

router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address_endpoint(payload: AddressCreate, db: Session = Depends(get_db)) -> AddressResponse:
    """Create a new address resource."""
    return create_address(db, payload)


@router.get("/", response_model=list[AddressResponse])
def list_addresses_endpoint(db: Session = Depends(get_db)) -> list[AddressResponse]:
    """Retrieve all address resources."""
    return list_addresses(db)


@router.get("/nearby", response_model=list[AddressResponse])
def nearby_addresses_endpoint(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    distance_km: float = Query(settings.default_nearby_distance_km, gt=0),
    db: Session = Depends(get_db),
) -> list[AddressResponse]:
    """Retrieve all addresses within a radius from an origin coordinate."""
    return find_nearby_addresses(db, latitude, longitude, distance_km)


@router.get("/{address_id}", response_model=AddressResponse)
def get_address_endpoint(address_id: int, db: Session = Depends(get_db)) -> AddressResponse:
    """Retrieve a single address by identifier."""
    return get_address_by_id(db, address_id)


@router.put("/{address_id}", response_model=AddressResponse)
def update_address_endpoint(
    address_id: int,
    payload: AddressUpdate,
    db: Session = Depends(get_db),
) -> AddressResponse:
    """Partially update an existing address."""
    return update_address(db, address_id, payload)


@router.delete("/{address_id}")
def delete_address_endpoint(address_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    """Delete an address by identifier."""
    delete_address(db, address_id)
    return {"message": "Address deleted successfully"}
