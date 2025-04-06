from pydantic import BaseModel


class BitcoinSummaryResponse(BaseModel):
    id: int
    max_price: float
    min_price: float
    date: str
