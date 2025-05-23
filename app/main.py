import os
from datetime import date

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router as bitcoin_router
from app.database.bitcoin_repository import BitcoinRepository
from app.dependencies import db_manager
from app.integration.email_sender_integration import EmailSenderIntegration
from app.jobs.bitcoin_price_cleaner_job import BitcoinPriceCleaner
from app.jobs.bitcoin_price_fetcher_job import BitcoinPriceFetcher
from app.service.bitcoin_price_api_service import BitcoinPriceApiService
from app.service.bitcoin_service import BitcoinService

# Initialization
app = FastAPI()

load_dotenv()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session = db_manager.get_session()
bitcoin_repository = BitcoinRepository(session)
bitcoin_service = BitcoinService(bitcoin_repository, date.today(), EmailSenderIntegration())
bitcoin_price_api_service = BitcoinPriceApiService(bitcoin_service, os.getenv("BITCOIN_API_URL"))

# Jobs
bitcoin_price_fetcher_job = BitcoinPriceFetcher(bitcoin_price_api_service)
bitcoin_price_cleaner_job = BitcoinPriceCleaner(bitcoin_repository)

# Include the router
app.include_router(bitcoin_router)

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("APP_HOST", "localhost"), port=os.getenv("APP_PORT", 8000))
