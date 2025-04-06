from datetime import datetime, date
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_bitcoin_service
from app.main import app

client = TestClient(app)


class MockBitcoinPrice:
    def __init__(self, id, price, timestamp):
        self.id = id
        self.price = price
        self.timestamp = timestamp


class MockSummary:
    def __init__(self, id, max_price, min_price, day):
        self.id = id
        self.max_price = max_price
        self.min_price = min_price
        self.day = day


@pytest.fixture
def mock_bitcoin_service(mocker):
    # Mock the BitcoinService dependency
    mock_service = MagicMock()
    app.dependency_overrides[get_bitcoin_service] = lambda: mock_service
    yield mock_service
    # Clean up after each test
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_latest_bitcoin_price_success(mock_bitcoin_service):
    # Arrange
    mock_price = MockBitcoinPrice(id=1, price=50000.0, timestamp=datetime(2025, 4, 6, 12, 0, 0))
    mock_bitcoin_service.get_latest_price.return_value = mock_price

    # Act
    response = client.get("/bitcoin/prices/latest")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "price": 50000.0,
        "timestamp": "2025-04-06 12:00:00"
    }


@pytest.mark.asyncio
async def test_get_latest_bitcoin_price_not_found(mock_bitcoin_service):
    # Arrange
    mock_bitcoin_service.get_latest_price.return_value = None

    # Act
    response = client.get("/bitcoin/prices/latest")

    # Assert
    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching latest price: 404: No prices found"}


@pytest.mark.asyncio
async def test_get_latest_bitcoin_price_error(mock_bitcoin_service):
    # Arrange
    mock_bitcoin_service.get_latest_price.side_effect = Exception("Database error")

    # Act
    response = client.get("/bitcoin/prices/latest")

    # Assert
    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching latest price: Database error"}


@pytest.mark.asyncio
async def test_get_summary_by_day_success(mock_bitcoin_service):
    # Arrange
    mock_summary = MockSummary(id=1, max_price=51000.0, min_price=49000.0, day=date(2025, 4, 6))
    mock_bitcoin_service.get_summary_by_date.return_value = mock_summary

    # Act
    response = client.get("/bitcoin/prices/summary/2025-04-06")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "max_price": 51000.0,
        "min_price": 49000.0,
        "date": "2025-04-06"  # Note: endpoint uses "date" instead of "day"
    }


@pytest.mark.asyncio
async def test_get_summary_by_day_not_found(mock_bitcoin_service):
    # Arrange
    mock_bitcoin_service.get_summary_by_date.return_value = None

    # Act
    response = client.get("/bitcoin/prices/summary/2025-04-06")

    # Assert
    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching summary: 404: No summary found for given date 2025-04-06"}


@pytest.mark.asyncio
async def test_get_summary_by_day_invalid_date(mock_bitcoin_service):
    # Act
    response = client.get("/bitcoin/prices/summary/invalid-date")

    # Assert
    assert response.status_code == 500  # FastAPI raises 500 for unhandled exceptions like ValueError
    assert "Error fetching summary" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_all_summaries_success(mock_bitcoin_service):
    # Arrange
    mock_summaries = [
        MockSummary(id=1, max_price=51000.0, min_price=49000.0, day=date(2025, 4, 6)),
        MockSummary(id=2, max_price=52000.0, min_price=50000.0, day=date(2025, 4, 7))
    ]
    mock_bitcoin_service.get_all_summaries.return_value = mock_summaries

    # Act
    response = client.get("/bitcoin/prices/summaries/")

    # Assert
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "max_price": 51000.0, "min_price": 49000.0, "date": "2025-04-06"},
        {"id": 2, "max_price": 52000.0, "min_price": 50000.0, "date": "2025-04-07"}
    ]


@pytest.mark.asyncio
async def test_get_all_summaries_empty(mock_bitcoin_service):
    # Arrange
    mock_bitcoin_service.get_all_summaries.return_value = []

    # Act
    response = client.get("/bitcoin/prices/summaries/")

    # Assert
    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching summary: 404: No summaries found!"}


@pytest.mark.asyncio
async def test_get_all_summaries_none(mock_bitcoin_service):
    # Arrange
    mock_bitcoin_service.get_all_summaries.return_value = None

    # Act
    response = client.get("/bitcoin/prices/summaries/")

    # Assert
    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching summary: 404: No summaries found!"}


@pytest.mark.asyncio
async def test_get_all_summaries_error(mock_bitcoin_service):
    # Arrange
    mock_bitcoin_service.get_all_summaries.side_effect = Exception("Database error")

    # Act
    response = client.get("/bitcoin/prices/summaries/")

    # Assert
    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching summary: Database error"}
