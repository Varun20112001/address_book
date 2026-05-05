"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from app.config import settings
from app.container import register_container
from app.database import Base, engine
from app.routers.address_controller import router as address_router


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
register_container(app)
app.include_router(address_router)

