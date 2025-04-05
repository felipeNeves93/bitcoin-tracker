from datetime import datetime

from sqlalchemy import Column, Integer, Float, DateTime

from app.database.database_manager import Base


class BitcoinPrice(Base):
    __tablename__ = "bitcoin_prices"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
