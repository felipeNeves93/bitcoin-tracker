from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from app.database.model.bitcoin_price import BitcoinPrice
from app.database.model.bitcoin_summary import BitcoinSummary


class BitcoinRepository:

    def __init__(self, db: Session):
        self.db = db

    def insert_price(self, price: float):
        bitcoin_price = BitcoinPrice(price=price)

        self.db.add(bitcoin_price)
        self.db.commit()
        self.db.refresh(bitcoin_price)

    def get_latest_price(self) -> Optional[BitcoinPrice]:
        return self.db.query(BitcoinPrice).order_by(BitcoinPrice.timestamp.desc()).first()

    def update_summary(self, max_price: float, min_price: float, day: date):
        existing_bitcoin_summary = self.db.query(BitcoinSummary).filter(
            BitcoinSummary.day == day).first()

        if existing_bitcoin_summary is None:
            print(f"Adding new summary for the day {day}")
            summary_to_add = BitcoinSummary(min_price=min_price, max_price=max_price, day=day)
            self.db.add(summary_to_add)
            self.db.commit()
            self.db.refresh(summary_to_add)

            return None

        print(f"Existing summary {existing_bitcoin_summary.id} for the day {day}. Updating prices")

        if existing_bitcoin_summary.max_price < max_price:
            existing_bitcoin_summary.max_price = max_price

        if existing_bitcoin_summary.min_price > min_price:
            existing_bitcoin_summary.min_price = min_price

        self.db.add(existing_bitcoin_summary)
        self.db.commit()
        self.db.refresh(existing_bitcoin_summary)

    def get_summary_by_day(self, day: date) -> Optional[BitcoinSummary]:
        return self.db.query(BitcoinSummary).filter(BitcoinSummary.day == day).first()
