"""API tests for the Address Book endpoints."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database() -> Generator[None, None, None]:
    """Prepare a fresh in-memory database for each test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override."""

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def sample_payload() -> dict[str, object]:
    """Return a baseline valid address payload."""
    return {
        "street": "123 Main St",
        "city": "New York",
        "state": "NY",
        "country": "USA",
        "zip_code": "10001",
        "latitude": 40.7128,
        "longitude": -74.0060,
    }


def test_create_address(client: TestClient) -> None:
    """Ensure a valid address can be created."""
    response = client.post("/addresses/", json=sample_payload())
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["city"] == "New York"


def test_create_address_invalid_coords(client: TestClient) -> None:
    """Ensure invalid coordinates are rejected by validation."""
    payload = sample_payload()
    payload["latitude"] = 200
    response = client.post("/addresses/", json=payload)
    assert response.status_code == 422


def test_get_all_addresses(client: TestClient) -> None:
    """Ensure all addresses endpoint returns a list."""
    client.post("/addresses/", json=sample_payload())
    response = client.get("/addresses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_address_by_id(client: TestClient) -> None:
    """Ensure an address can be fetched by id."""
    created = client.post("/addresses/", json=sample_payload()).json()
    response = client.get(f"/addresses/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_address_not_found(client: TestClient) -> None:
    """Ensure missing address requests return 404."""
    response = client.get("/addresses/9999")
    assert response.status_code == 404


def test_update_address(client: TestClient) -> None:
    """Ensure partial updates modify only provided fields."""
    created = client.post("/addresses/", json=sample_payload()).json()
    response = client.put(f"/addresses/{created['id']}", json={"city": "Boston"})
    assert response.status_code == 200
    assert response.json()["city"] == "Boston"


def test_delete_address(client: TestClient) -> None:
    """Ensure an address can be deleted successfully."""
    created = client.post("/addresses/", json=sample_payload()).json()
    response = client.delete(f"/addresses/{created['id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Address deleted successfully"


def test_nearby_addresses(client: TestClient) -> None:
    """Ensure nearby endpoint filters addresses by distance."""
    payload_near = sample_payload()
    payload_far = sample_payload()
    payload_far.update({"street": "999 Far Ave", "city": "Los Angeles", "latitude": 34.0522, "longitude": -118.2437})

    client.post("/addresses/", json=payload_near)
    client.post("/addresses/", json=payload_far)

    response = client.get(
        "/addresses/nearby",
        params={"latitude": 40.7128, "longitude": -74.0060, "distance_km": 20},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["city"] == "New York"
