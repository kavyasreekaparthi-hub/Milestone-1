from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional
from decimal import Decimal

# Base properties shared by all Transaction schemas
class TransactionBase(BaseModel):
    account_id: int
    description: str
    category: str
    amount: Decimal
    currency: str = "USD"
    txn_type: str  # e.g., "credit" or "debit"
    merchant: Optional[str] = None
    txn_date: date
    posted_date: Optional[date] = None

# Schema for creating a transaction (used for CSV imports)
class TransactionCreate(TransactionBase):
    pass

# Schema for reading a transaction (what the API returns)
class Transaction(TransactionBase):
    id: int
    
    # Allows Pydantic to read data from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)