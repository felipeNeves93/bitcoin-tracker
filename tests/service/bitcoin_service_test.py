from datetime import date
from unittest.mock import MagicMock

from app.database.bitcoin_repository import BitcoinRepository
from app.service.bitcoin_service import BitcoinService


def test_create_new_summary_cache():
    mock_repo = MagicMock(spec=BitcoinRepository)
    mock_repo.update_summary.return_value = None

    cache_date = date(2021, 1, 1)

    bitcoin_service: BitcoinService = BitcoinService(mock_repo, cache_date)
    cached_summary = bitcoin_service.get_cached_summary()

    assert cached_summary['current_date'] == cache_date
    assert cached_summary['min_price'] == 999_999_999
    assert cached_summary['max_price'] == 0

    bitcoin_service.update_summary(100)
    cached_summary = bitcoin_service.get_cached_summary()

    assert cached_summary['current_date'] == date.today()
    assert cached_summary['min_price'] == 100
    assert cached_summary['max_price'] == 100


def test_update_max_price_from_summary_cache():
    mock_repo = MagicMock(spec=BitcoinRepository)
    mock_repo.update_summary.return_value = None

    cache_date = date.today()

    bitcoin_service: BitcoinService = BitcoinService(mock_repo, cache_date)

    bitcoin_service.update_summary(100)
    bitcoin_service.update_summary(900)
    cached_summary = bitcoin_service.get_cached_summary()

    assert cached_summary['current_date'] == cache_date
    assert cached_summary['min_price'] == 100
    assert cached_summary['max_price'] == 900


def test_update_min_price_from_summary_cache():
    mock_repo = MagicMock(spec=BitcoinRepository)
    mock_repo.update_summary.return_value = None

    cache_date = date.today()

    bitcoin_service: BitcoinService = BitcoinService(mock_repo, cache_date)

    bitcoin_service.update_summary(100)
    bitcoin_service.update_summary(50)
    cached_summary = bitcoin_service.get_cached_summary()

    assert cached_summary['current_date'] == cache_date
    assert cached_summary['min_price'] == 50
    assert cached_summary['max_price'] == 100
