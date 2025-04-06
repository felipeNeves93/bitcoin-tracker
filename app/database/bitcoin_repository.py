import datetime
from datetime import date, datetime, timedelta
from typing import Optional, Type

from sqlalchemy.orm import Session

from app.database.model.bitcoin_price import BitcoinPrice
from app.database.model.bitcoin_summary import BitcoinSummary


class BitcoinRepository:

    def __init__(self, db: Session):
        self.db = db

    def insert_price(self, price: float, timestamp=None):
        bitcoin_price = BitcoinPrice(price=price, timestamp=timestamp)

        self.db.add(bitcoin_price)
        self.db.commit()
        self.db.refresh(bitcoin_price)

    def get_latest_price(self) -> Optional[BitcoinPrice]:
        return self.db.query(BitcoinPrice).order_by(BitcoinPrice.timestamp.desc()).first()

    def update_summary(self, price: float, day: date):
        existing_bitcoin_summary = self.db.query(BitcoinSummary).filter(
            BitcoinSummary.day == day).first()

        if existing_bitcoin_summary is None:
            print(f"Adding new summary for the day {day}")
            summary_to_add = BitcoinSummary(min_price=price, max_price=price, day=day)
            self.db.add(summary_to_add)
            self.db.commit()
            self.db.refresh(summary_to_add)

            return None

        print(f"Existing summary {existing_bitcoin_summary.id} for the day {day}. Updating prices if needed")

        if existing_bitcoin_summary.max_price < price:
            existing_bitcoin_summary.max_price = price

        if existing_bitcoin_summary.min_price > price:
            existing_bitcoin_summary.min_price = price

        self.db.add(existing_bitcoin_summary)
        self.db.commit()
        self.db.refresh(existing_bitcoin_summary)

    def get_summary_by_day(self, day: date) -> Optional[BitcoinSummary]:
        return self.db.query(BitcoinSummary).filter(BitcoinSummary.day == day).first()

    def get_all_summaries(self) -> list[Type[BitcoinSummary]]:
        return self.db.query(BitcoinSummary).all()

    def delete_prices_older_than_90_days(self):
        date_to_delete = datetime.now() - timedelta(days=90)

        print(f"Date to cut: {date_to_delete}")

        result = self.db.query(BitcoinPrice).filter(BitcoinPrice.timestamp < date_to_delete).delete()
        self.db.commit()

        return result

    def get_all_prices(self) -> list[type[BitcoinPrice]]:
        return self.db.query(BitcoinPrice).all()
