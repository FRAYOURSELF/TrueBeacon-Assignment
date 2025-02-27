from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.models import Tick, Bhavcopy
from backend.database import SessionLocal, ticks, bhavcopy
from backend.services import ingest_ticks_data  # Import function from services.py
from fastapi.middleware.cors import CORSMiddleware
from backend.services import ingest_bhavcopy_data  # Import function from services.py


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    # Path to your zip file containing ticks data
    ticks_data_path = 'data/ticks_data.zip'
    ingest_ticks_data(ticks_data_path)  # No 'await' if function is synchronous

    # Path to your zip file containing Bhavcopy data
    bhavcopy_data_path = 'data/bhavcopy_eodsnapshot_data.zip'
    ingest_bhavcopy_data(bhavcopy_data_path)




# Query optimization by batching and limiting results
from sqlalchemy import select
@app.get("/ticks")
def get_ticks(db: Session = Depends(get_db)):
    stmt = select(ticks).order_by(ticks.c.timestamp.desc()).limit(1000)
    result = db.execute(stmt).fetchall()
    return [{"symbol": row.symbol, "timestamp": row.timestamp, "price": row.price, "quantity": row.quantity} for row in result]


@app.get("/bhavcopy", response_model=list[Bhavcopy])
async def get_bhavcopy(db: Session = Depends(get_db)):
    # Query data from the database
    result = db.execute(select(bhavcopy)).fetchall()
    return [
        Bhavcopy(symbol=row.symbol, close_price=row.close_price, timestamp=row.timestamp)
        for row in result
    ]

class OrderRequest(BaseModel):
    symbol: str
    price: float
    quantity: int

@app.post("/place-order")
def place_order(order: OrderRequest, db: Session = Depends(get_db)):
    # Insert order into ticks table as a mock order
    db.execute(ticks.insert().values(
        symbol=order.symbol,
        timestamp="2025-02-19 10:00:00",
        price=order.price,
        quantity=order.quantity
    ))
    db.commit()
    return {"message": f"Order placed for {order.symbol} at {order.price} for {order.quantity} shares"}