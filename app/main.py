"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from app.config import settings
from app.database import Base, engine


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] [%(asctime)s] - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Create database tables when the application starts."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created or already exist")
    yield


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)

