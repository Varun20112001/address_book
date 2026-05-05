"""Router module for address-related API endpoints."""

from fastapi import APIRouter, Depends, Query, status

from app.config import settings
from app.providers import get_address_service
from app.schemas.address import AddressCreate, AddressResponse, AddressUpdate
from app.services.address_service import AddressService

router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address_endpoint(
    payload: AddressCreate,
    address_service: AddressService = Depends(get_address_service),
) -> AddressResponse:
    """Create a new address resource."""
    return address_service.create_address(payload)


@router.get("/", response_model=list[AddressResponse])
def list_addresses_endpoint(address_service: AddressService = Depends(get_address_service)) -> list[AddressResponse]:
    """Retrieve all address resources."""
    return address_service.list_addresses()


@router.get("/nearby", response_model=list[AddressResponse])
def nearby_addresses_endpoint(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    distance_km: float = Query(settings.default_nearby_distance_km, gt=0),
    address_service: AddressService = Depends(get_address_service),
) -> list[AddressResponse]:
    """Retrieve all addresses within a radius from an origin coordinate."""
    return address_service.find_nearby_addresses(latitude, longitude, distance_km)


@router.get("/{address_id}", response_model=AddressResponse)
def get_address_endpoint(
    address_id: int,
    address_service: AddressService = Depends(get_address_service),
) -> AddressResponse:
    """Retrieve a single address by identifier."""
    return address_service.get_address_by_id(address_id)


@router.put("/{address_id}", response_model=AddressResponse)
def update_address_endpoint(
    address_id: int,
    payload: AddressUpdate,
    address_service: AddressService = Depends(get_address_service),
) -> AddressResponse:
    """Partially update an existing address."""
    return address_service.update_address(address_id, payload)


@router.delete("/{address_id}")
def delete_address_endpoint(
    address_id: int,
    address_service: AddressService = Depends(get_address_service),
) -> dict[str, str]:
    """Delete an address by identifier."""
    address_service.delete_address(address_id)
    return {"message": "Address deleted successfully"}
