# Address Book REST API

A production-ready Address Book REST API built with FastAPI, SQLAlchemy (sync), and SQLite.
The API supports creating, updating, deleting, listing, and nearby-distance search for addresses.
The codebase is organized with controller, service, use case, repository, and provider/container layers.

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy (sync)
- SQLite
- Pydantic v2
- geopy
- uvicorn
- python-dotenv
- pytest + httpx

## Setup & Run

```bash
# Clone / enter directory
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Docs

http://127.0.0.1:8000/docs

## Run Tests

```bash
pytest tests/ -v
```

## Project Structure

```text
address_book/
|-- app/
|   |-- main.py
|   |-- config.py
|   |-- container.py
|   |-- database.py
|   |-- providers.py
|   |-- models/
|   |   `-- address.py
|   |-- repositories/
|   |   `-- address_repository.py
|   |-- routers/
|   |   `-- address_controller.py
|   |-- schemas/
|   |   `-- address.py
|   |-- services/
|   |   `-- address_service.py
|   |-- usecases/
|   |   `-- address_usecases.py
|   `-- utils/
|       `-- geo.py
|-- tests/
|   `-- test_addresses.py
|-- requirements.txt
`-- README.md
```

## Architecture

- `main.py` creates the FastAPI app, registers the application container, creates database tables on startup, and includes the address router.
- `container.py` builds application dependencies such as repositories, use cases, and services.
- `providers.py` exposes FastAPI dependency providers, including `get_address_service`.
- `routers/address_controller.py` defines the HTTP endpoints and depends on `AddressService`.
- `services/address_service.py` is the controller-facing facade for address operations.
- `usecases/address_usecases.py` contains application/business rules, including not-found handling and nearby-distance filtering.
- `repositories/address_repository.py` contains the abstract repository contract and the SQLAlchemy implementation. All address database queries and commit/rollback operations live here.

## API Endpoints and Example cURL Commands

### 1) Create Address

- **POST** `/addresses/`

```bash
curl -X POST "http://127.0.0.1:8000/addresses/" \
  -H "Content-Type: application/json" \
  -d '{
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "country": "USA",
    "zip_code": "10001",
    "latitude": 40.7128,
    "longitude": -74.0060
  }'
```

### 2) List Addresses

- **GET** `/addresses/`

```bash
curl "http://127.0.0.1:8000/addresses/"
```

### 3) Get Address by ID

- **GET** `/addresses/{address_id}`

```bash
curl "http://127.0.0.1:8000/addresses/1"
```

### 4) Update Address (Partial)

- **PUT** `/addresses/{address_id}`

```bash
curl -X PUT "http://127.0.0.1:8000/addresses/1" \
  -H "Content-Type: application/json" \
  -d '{"city": "Boston"}'
```

### 5) Delete Address

- **DELETE** `/addresses/{address_id}`

```bash
curl -X DELETE "http://127.0.0.1:8000/addresses/1"
```

### 6) Nearby Addresses

- **GET** `/addresses/nearby?latitude=X&longitude=Y&distance_km=Z`

```bash
curl "http://127.0.0.1:8000/addresses/nearby?latitude=40.7128&longitude=-74.0060&distance_km=10"
```
