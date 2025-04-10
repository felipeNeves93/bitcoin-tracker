from threading import Event, Thread

from app.database.bitcoin_repository import BitcoinRepository


class BitcoinPriceCleaner:

    def __init__(self, bitcoin_repository: BitcoinRepository):
        self._stop_event = Event()
        self._thread = None
        self.bitcoin_repository = bitcoin_repository
        self.start_job()

    def _run_job(self):
        while not self._stop_event.wait(86400):
            print("Removing bitcoin prices older than 90 days!")
            self.bitcoin_repository.delete_prices_older_than_90_days()

    def start_job(self):
        if not self._thread or not self._thread._is_alive():
            self._stop_event.clear()
            self._thread = Thread(target=self._run_job)
            self._thread.daemon = True
            self._thread.start()
            print("BitcoinPriceCleaner job started!")

    def stop_job(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        print("BitcoinPriceCleaner job stopped!")
