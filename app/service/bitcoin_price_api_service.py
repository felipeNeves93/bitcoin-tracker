import requests

from app.service.bitcoin_service import BitcoinService


class BitcoinPriceApiService:

    def __init__(self, bitcoin_service: BitcoinService, api_url):
        self.bitcoin_service = bitcoin_service
        self.api_url = api_url

    def fetch_latest_price(self):
        try:
            print(f"Fetching bitcoin price from {self.api_url}")
            response = requests.get(self.api_url)
            response.raise_for_status()

            data = response.json()
            bitcoin_price: float = float(data["bitcoin"]["usd"])

            print(f"Price of {bitcoin_price} fetched successfully! Updating database")
            self.bitcoin_service.update_price(bitcoin_price)

            return bitcoin_price

        except Exception as e:
            print(f"An error occurred while fetching bitcoin price from the {self.api_url}! {e}")
            return None
