from pydantic import BaseModel


class BitcoinPriceResponse(BaseModel):
    id: int
    price: float
    timestamp: str
