import os
from datetime import date

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from app.database.bitcoin_repository import BitcoinRepository
from app.database.database_manager import DatabaseManager
from app.jobs.bitcoin_price_fetcher_job import BitcoinPriceFetcher
from app.service.bitcoin_price_api_service import BitcoinPriceApiService
from app.service.bitcoin_service import BitcoinService

# Initialization
app = FastAPI()
load_dotenv()

# DB
db_manager = DatabaseManager()
session = db_manager.get_session()

# Services and repos
bitcoin_repository = BitcoinRepository(session)

bitcoin_service = BitcoinService(bitcoin_repository, date.today())
bitcoin_price_api_service = BitcoinPriceApiService(bitcoin_service, os.getenv("BITCOIN_API_URL"))

# Jobs
bitcoin_price_fetcher_job = BitcoinPriceFetcher(bitcoin_price_api_service)


@app.on_event("shutdown")
def shutdown_event():
    bitcoin_price_fetcher_job.stop_job()


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("APP_HOST", "localhost"), port=os.getenv("APP_PORT", 8000))
