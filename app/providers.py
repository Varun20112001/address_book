"""FastAPI dependency providers."""

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.container import ApplicationContainer
from app.database import get_db
from app.services.address_service import AddressService


def get_container(request: Request) -> ApplicationContainer:
    """Resolve the registered application container."""
    return request.app.state.container


def get_address_service(
    db: Session = Depends(get_db),
    container: ApplicationContainer = Depends(get_container),
) -> AddressService:
    """Resolve an address service for the current request."""
    return container.address_service(db)
