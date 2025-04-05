from datetime import date

from app.database.bitcoin_repository import BitcoinRepository


class BitcoinService:
    _bitcoin_summary_cache = {}
    _curr_date = None

    def __init__(self, repository: BitcoinRepository, current_date: date):
        self.repository = repository
        self._curr_date = current_date
        self._bitcoin_summary_cache = {'min_price': 999_999_999.0,
                                       'max_price': 0.0,
                                       'current_date': self._curr_date}

    def insert_price(self, price: float):
        try:
            print(f"Inserting new price for bitcoin {price}")
            self.repository.insert_price(price)

            self.update_summary(price)
        except Exception as e:
            print(f"An error occurred while inserting price: {e}")

    def update_summary(self, price: float):
        try:
            print("Updating bitcoin summary")
            today = date.today()
            if self._curr_date < today:
                self.repository.update_summary(price, today)
                self._create_new_summary_cache(price, today)

                return None

            if self._should_update_summary(price):
                self._update_cache(price)
                self.repository.update_summary(price, today)
        except Exception as e:
            print(f"An error happened while updating summary: {e}")

    def _create_new_summary_cache(self, price: float, cache_date: date):
        self._curr_date = cache_date

        print(f"Creating new bitcoin summary cache for {cache_date}")
        self._bitcoin_summary_cache['min_price'] = price
        self._bitcoin_summary_cache['max_price'] = price
        self._bitcoin_summary_cache['current_date'] = cache_date

    def _should_update_summary(self, price: float):
        return (self._bitcoin_summary_cache['min_price'] > price or
                self._bitcoin_summary_cache['max_price'] < price)

    def _update_cache(self, price: float):
        if self._bitcoin_summary_cache['min_price'] > price:
            print(f"Updating the min value of the cache with the new low: {price}")
            self._bitcoin_summary_cache['min_price'] = price

        if self._bitcoin_summary_cache['max_price'] < price:
            print(f"Updating the max value of the cache with the new max: {price}")
            self._bitcoin_summary_cache['max_price'] = price

    def get_cached_summary(self) -> dict:
        return self._bitcoin_summary_cache
