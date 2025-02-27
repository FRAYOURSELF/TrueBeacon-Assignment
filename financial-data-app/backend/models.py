from pydantic import BaseModel
from datetime import datetime

class Tick(BaseModel):
    symbol: str
    timestamp: datetime
    price: float
    quantity: int

    class Config:
        orm_mode = True

class Bhavcopy(BaseModel):
    symbol: str
    close_price: float
    timestamp: str  # Changed from datetime to str

    class Config:
        orm_mode = True
