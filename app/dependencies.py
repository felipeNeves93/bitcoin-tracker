import os
from datetime import date

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.bitcoin_repository import BitcoinRepository
from app.database.database_manager import DatabaseManager
from app.service.bitcoin_price_api_service import BitcoinPriceApiService
from app.service.bitcoin_service import BitcoinService

db_manager = DatabaseManager()


# Dependency functions
def get_session() -> Session:
    return db_manager.get_session()


def get_bitcoin_repository(session: Session = Depends(get_session)) -> BitcoinRepository:
    return BitcoinRepository(session)


def get_bitcoin_service(repository: BitcoinRepository = Depends(get_bitcoin_repository)) -> BitcoinService:
    return BitcoinService(repository, date.today())


def get_bitcoin_price_api_service(
        bitcoin_service: BitcoinService = Depends(get_bitcoin_service)) -> BitcoinPriceApiService:
    return BitcoinPriceApiService(bitcoin_service, os.getenv("BITCOIN_API_URL"))
