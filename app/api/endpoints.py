from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from app.api.responses.bitcoin_price_response import BitcoinPriceResponse
from app.api.responses.bitcoin_summary_response import BitcoinSummaryResponse
from app.dependencies import get_bitcoin_service
from app.service.bitcoin_service import BitcoinService

router = APIRouter(prefix="/bitcoin", tags=["bitcoin"])


@router.get("/prices/latest", response_model=BitcoinPriceResponse)
async def get_latest_bitcoin_price(bitcoin_service: BitcoinService = Depends(get_bitcoin_service)):
    try:
        latest_price = bitcoin_service.get_latest_price()
        if latest_price is None:
            raise HTTPException(status_code=404, detail="No prices found")
        return BitcoinPriceResponse(id=latest_price.id, price=latest_price.price,
                                    timestamp=latest_price.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching latest price: {str(e)}")


@router.get("/prices/summary/{date}", response_model=BitcoinSummaryResponse)
async def get_summary_by_day(date: str, bitcoin_service: BitcoinService = Depends(get_bitcoin_service)):
    try:
        converted_date = datetime.strptime(date, "%Y-%m-%d").date()
        summary = bitcoin_service.get_summary_by_date(converted_date)
        if summary is None:
            return BitcoinSummaryResponse(id=0, max_price=0.0, min_price=0.0,
                                          date=date)
        return BitcoinSummaryResponse(id=summary.id, max_price=summary.max_price, min_price=summary.min_price,
                                      date=summary.day.strftime("%Y-%m-%d"))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error fetching summary: {str(e)}")


@router.get("/prices/summaries", response_model=list[BitcoinSummaryResponse])
async def get_all_summaries(bitcoin_service: BitcoinService = Depends(get_bitcoin_service)):
    try:
        summaries = bitcoin_service.get_all_summaries()
        if summaries is None or len(summaries) == 0:
            raise HTTPException(status_code=404, detail="No summaries found!")
        return [BitcoinSummaryResponse(id=summary.id, max_price=summary.max_price, min_price=summary.min_price,
                                       date=summary.day.strftime("%Y-%m-%d")) for summary in summaries]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error fetching summary: {str(e)}")
