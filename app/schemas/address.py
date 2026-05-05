"""Pydantic schemas for address payloads and responses."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class AddressBase(BaseModel):
    """Base address schema with shared fields and coordinate validators."""

    street: str
    city: str
    state: str
    country: str
    zip_code: str
    latitude: float
    longitude: float

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, value: float) -> float:
        """Validate that latitude is within [-90, 90]."""
        if not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, value: float) -> float:
        """Validate that longitude is within [-180, 180]."""
        if not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return value


class AddressCreate(AddressBase):
    """Schema for creating a new address."""


class AddressUpdate(BaseModel):
    """Schema for partially updating an address."""

    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, value: Optional[float]) -> Optional[float]:
        """Validate that latitude is within [-90, 90] when provided."""
        if value is not None and not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, value: Optional[float]) -> Optional[float]:
        """Validate that longitude is within [-180, 180] when provided."""
        if value is not None and not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return value


class AddressResponse(AddressBase):
    """Schema returned to API consumers for address resources."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
