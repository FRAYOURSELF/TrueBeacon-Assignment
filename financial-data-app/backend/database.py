# Optimized database schema
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Index, MetaData, Table
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://app_user:password@localhost:5432/financial_db"

# Connect to the database with optimizations
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData()

# Optimized ticks table
ticks = Table('ticks', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('symbol', String(50), nullable=False, index=True),
    Column('timestamp', DateTime, nullable=False, index=True),
    Column('price', Float, nullable=False),
    Column('quantity', Integer, nullable=False)
)
Index('idx_symbol_timestamp', ticks.c.symbol, ticks.c.timestamp)

bhavcopy = Table('bhavcopy', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('symbol', String(50), nullable=False, index=True),
    Column('close_price', Float, nullable=False),
    Column('timestamp', String(20), nullable=False, index=True)  # Changed to String
)

# Create tables with optimized indexes
metadata.create_all(engine)