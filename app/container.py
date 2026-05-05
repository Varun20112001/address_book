"""Application dependency container."""

from sqlalchemy.orm import Session

from app.repositories.address_repository import SqlAlchemyAddressRepository
from app.services.address_service import AddressService
from app.usecases.address_usecases import AddressUseCases


class ApplicationContainer:
    """Factory container for application services."""

    def address_repository(self, db: Session) -> SqlAlchemyAddressRepository:
        """Provide an address repository for the current database session."""
        return SqlAlchemyAddressRepository(db)

    def address_use_cases(self, db: Session) -> AddressUseCases:
        """Provide address use cases with their repository dependency."""
        return AddressUseCases(repository=self.address_repository(db))

    def address_service(self, db: Session) -> AddressService:
        """Provide the address service with its use case dependency."""
        return AddressService(use_cases=self.address_use_cases(db))


def register_container(app: object) -> ApplicationContainer:
    """Register the application container on the FastAPI app state."""
    container = ApplicationContainer()
    app.state.container = container
    return container
