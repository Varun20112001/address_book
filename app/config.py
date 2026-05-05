"""Application configuration module."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    app_name: str = os.getenv("APP_NAME", "Address Book API")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    db_url: str = os.getenv("DATABASE_URL", "sqlite:///./address_book.db")
    default_nearby_distance_km: float = float(os.getenv("DEFAULT_NEARBY_DISTANCE_KM", "10.0"))


settings = Settings()
