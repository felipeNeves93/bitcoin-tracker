from unittest.mock import MagicMock

from app.service.api_integration_service import ApiIntegrationService
from app.service.bitcoin_service import BitcoinService


def test_get_latest_price():
    coin_gecko_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    bitcoin_service = MagicMock(spec=BitcoinService)
    bitcoin_service.insert_price.return_value = None

    api_integration_service = ApiIntegrationService(bitcoin_service, coin_gecko_url)

    bitcoin_value = api_integration_service.get_latest_bitcoin_value()

    assert bitcoin_value is not None
