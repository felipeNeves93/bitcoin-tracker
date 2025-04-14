import os
from datetime import date, timedelta
from typing import Optional

from app.database.bitcoin_repository import BitcoinRepository
from app.database.model.bitcoin_price import BitcoinPrice
from app.database.model.bitcoin_summary import BitcoinSummary
from app.integration.email_sender_integration import EmailSenderIntegration


class BitcoinService:
    _bitcoin_summary_cache = {}
    _curr_date = None

    def __init__(self, repository: BitcoinRepository, current_date: date, email_sender: EmailSenderIntegration):
        self.repository = repository
        self.email_sender = email_sender
        self._curr_date = current_date
        self._bitcoin_summary_cache = {'min_price': 999_999_999.0,
                                       'max_price': 0.0,
                                       'current_date': self._curr_date}
        self.current_price = 0.0
        self.max_historic_price = 0.0
        self.bitcoin_price_dip_threshold = os.getenv("bitcoin_price_dip_min_threshold")

    def update_price(self, price: float):

        """
        Updates the price of bitcoin.

        This method inserts a new price for bitcoin in the database, updates the summary for the current date and notifies by email if the price has dipped.
        If an error occurs while inserting the price, it logs the error.

        :param price: The current price of bitcoin
        :return: None
        """
        try:
            print(f"Inserting new price for bitcoin {price}")
            self.repository.insert_price(price)

            self.update_summary(price)
        except Exception as e:
            print(f"An error occurred while inserting price: {e}")

    def update_summary(self, price: float):
        """
        Updates the bitcoin summary for the current date.

        This method checks if the current date has changed. If it has, it creates a new cache for the new date.
        It also checks if the current price is lower than the minimum price stored in the cache or higher than the maximum price stored in the cache.
        If the price is lower or higher than the values stored in the cache, it updates the cache with the new values and updates the summary in the database.

        :param price: The current price of bitcoin
        :return: None
        """
        try:
            print("Updating bitcoin summary")
            today = date.today()
            if self._curr_date < today:
                self.repository.update_summary(price, today)
                self._create_new_cache(price, today)

                return None

            if self._should_update_summary(price):
                self._update_cache(price)
                self.repository.update_summary(price, today)
        except Exception as e:
            print(f"An error happened while updating summary: {e}")

    def _create_new_cache(self, price: float, cache_date: date):
        """
        Creates a new cache for the given date with the given price.

        This method is called when the current date changes and a new cache needs to be created for the new date.
        It sets the current date, the current price and the max_historic_price for the new cache.

        :param price: The price to be used for the new cache
        :param cache_date: The date for which the new cache should be created
        :return: None
        """
        print(f"Creating new bitcoin  cache for {cache_date}")
        self._curr_date = cache_date
        ninety_days_ago = cache_date - timedelta(days=90)

        self.current_price = price
        self.max_historic_price = self.repository.get_max_historic_price(start_date=ninety_days_ago)

        self._bitcoin_summary_cache['min_price'] = price
        self._bitcoin_summary_cache['max_price'] = price
        self._bitcoin_summary_cache['current_date'] = cache_date

    def _should_update_summary(self, price: float):
        return (self._bitcoin_summary_cache['min_price'] > price or
                self._bitcoin_summary_cache['max_price'] < price)

    def _update_cache(self, price: float):
        print("Updating cache")
        self.current_price = price

        if price > self.max_historic_price:
            print(f"Updating max_historic_price with new price {price}")
            self.max_historic_price = price

        if self._bitcoin_summary_cache['min_price'] > price:
            self._bitcoin_summary_cache['min_price'] = price

        if self._bitcoin_summary_cache['max_price'] < price:
            self._bitcoin_summary_cache['max_price'] = price

    def get_cached_summary(self) -> dict:
        return self._bitcoin_summary_cache

    def get_latest_price(self) -> Optional[BitcoinPrice]:
        return self.repository.get_latest_price()

    def get_summary_by_date(self, day: date) -> Optional[BitcoinSummary]:
        return self.repository.get_summary_by_day(day)

    def get_all_summaries(self) -> list[type[BitcoinSummary]]:
        return self.repository.get_all_summaries()

    def notify_email_bitcoin_price_dip(self):
        """
        Notify by email when the current bitcoin price is lower than the lowest price of the last 90 days.

        This method checks if the current bitcoin price is lower than the lowest price of the last 90 days.
        If it is, it sends an email with the current price and a suggestion to buy bitcoin.
        """
        if self._should_notify():
            print("Notifying via email lowest price of bitcoin in the last 90 days")
            destination_email = os.getenv("DESTINATION_EMAIL")
            email_message = (f"There is a new low in the bitcoin price ${self.current_price}. "
                             f"It is the lowest price of the last 90 days. Perhaps is a good time to buy ")
            subject = "Time to buy bitcoin"

            self.email_sender.send_email(email_message, subject, destination_email)

    def _should_notify(self) -> bool:
        """
        Determines whether a notification should be sent based on the current bitcoin price.

        This method checks if the current bitcoin price has dipped below a certain
        threshold compared to the maximum historic price. The threshold is determined
        as a percentage of the maximum historic price, retrieved from an environment
        variable. If the price dip exceeds this threshold, a notification is warranted.

        :return: True if the price dip exceeds the threshold and a notification should be sent, False otherwise.
        """
        if self.max_historic_price <= 0:
            return False

        percentual_value_threshold = float(os.getenv("BITCOIN_PRICE_DIP_MIN_THRESHOLD", 0.1) * self.max_historic_price)
        variation = (self.max_historic_price - self.current_price) - percentual_value_threshold

        return variation >= 0
