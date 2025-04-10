import datetime
from datetime import date, datetime, timedelta
from typing import Optional, Type

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.model.bitcoin_price import BitcoinPrice
from app.database.model.bitcoin_summary import BitcoinSummary


class BitcoinRepository:

    def __init__(self, session: Session):
        self.session = session

    def insert_price(self, price: float, timestamp=None):
        bitcoin_price = BitcoinPrice(price=price, timestamp=timestamp)

        self.session.add(bitcoin_price)
        self.session.commit()
        self.session.refresh(bitcoin_price)

    def get_latest_price(self) -> Optional[BitcoinPrice]:
        try:
            return self.session.query(BitcoinPrice).order_by(BitcoinPrice.timestamp.desc()).first()
        finally:
            self.session.close()

    def update_summary(self, price: float, day: date):
        try:
            existing_bitcoin_summary = self.session.query(BitcoinSummary).filter(
                BitcoinSummary.day == day).first()

            if existing_bitcoin_summary is None:
                print(f"Adding new summary for the day {day}")
                summary_to_add = BitcoinSummary(min_price=price, max_price=price, day=day)
                self.session.add(summary_to_add)
                self.session.commit()
                self.session.refresh(summary_to_add)

                return None

            print(f"Existing summary {existing_bitcoin_summary.id} for the day {day}. Updating prices if needed")

            if existing_bitcoin_summary.max_price < price:
                existing_bitcoin_summary.max_price = price

            if existing_bitcoin_summary.min_price > price:
                existing_bitcoin_summary.min_price = price

            self.session.add(existing_bitcoin_summary)
            self.session.commit()
            self.session.refresh(existing_bitcoin_summary)
        finally:
            self.session.close()

    def get_summary_by_day(self, day: date) -> Optional[BitcoinSummary]:
        try:
            return self.session.query(BitcoinSummary).filter(BitcoinSummary.day == day).first()
        finally:
            self.session.close()

    def get_all_summaries(self) -> list[Type[BitcoinSummary]]:
        try:
            return self.session.query(BitcoinSummary).all()
        finally:
            self.session.close()

    def delete_prices_older_than_90_days(self):
        try:
            date_to_delete = datetime.now() - timedelta(days=90)

            print(f"Date to cut: {date_to_delete}")

            result = self.session.query(BitcoinPrice).filter(BitcoinPrice.timestamp < date_to_delete).delete()
            self.session.commit()

            return result
        finally:
            self.session.close()

    def get_all_prices(self) -> list[type[BitcoinPrice]]:
        try:
            return self.session.query(BitcoinPrice).all()
        finally:
            self.session.close()

    def get_max_historic_price(self, start_date: date, end_date: date = date.today()) -> Optional[float]:
        try:
            period_length = (end_date - start_date).days
            if period_length > 90:
                raise ValueError("Period should not exceed 90 days!")
            if period_length < 0:
                raise ValueError("Start date must be before or equal end date!")
            return (self.session.query(func.max(BitcoinSummary.max_price))
                    .filter(BitcoinSummary.day <= end_date)
                    .filter(BitcoinSummary.day >= start_date)
                    .scalar())
        finally:
            self.session.close()
