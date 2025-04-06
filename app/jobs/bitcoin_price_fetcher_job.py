from threading import Event, Thread

from app.service.bitcoin_price_api_service import BitcoinPriceApiService


class BitcoinPriceFetcher:

    def __init__(self, bitcoin_price_api_service: BitcoinPriceApiService):
        self._stop_event = Event()
        self._thread = None
        self.bitcoin_price_api_service = bitcoin_price_api_service
        self.start_job()

    def _run_job(self):
        while not self._stop_event.wait(60):
            print("Fetching latest bitcoin price each 60 seconds")
            self.bitcoin_price_api_service.fetch_latest_price()

    def start_job(self):
        if not self._thread or not self._thread._is_alive():
            self._stop_event.clear()
            self._thread = Thread(target=self._run_job)
            self._thread.start()
            print("BitcoinPriceFetcher job started!")

    def stop_job(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        print("BitcoinPriceFetcher job stopped!")
