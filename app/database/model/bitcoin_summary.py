from sqlalchemy import Column, Integer, Float, Date

from app.database.database_manager import Base


class BitcoinSummary(Base):
    __tablename__ = "bitcoin_summary"

    id = Column(Integer, primary_key=True, index=True)
    max_price = Column(Float, nullable=False)
    min_price = Column(Float)
    day = Column(Date, unique=True, index=True)
