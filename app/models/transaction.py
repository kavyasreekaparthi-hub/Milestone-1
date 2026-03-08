<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

# --- MODEL 1: TRANSACTIONS ---
class Transaction(Base):
    __tablename__ = "transactions"

    # --- PRIMARY KEYS & IDENTITY ---
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # --- BANKING DATA ---
    account_id = Column(Integer, index=True, nullable=True) 
    merchant = Column(String, index=True) 
    
    # --- CORE FINANCIAL DATA ---
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    # 'debit' for spending, 'credit' for income
    transaction_type = Column(String, default="debit") 
    
    # --- DATES ---
    transaction_date = Column(DateTime, server_default=func.now())
    posted_date = Column(DateTime, nullable=True) 
    
    # --- INTELLIGENCE ENGINE DATA ---
    description = Column(String)  # The Rule Engine scans this field
    category = Column(String, default="Uncategorized") 

# --- MODEL 2: CATEGORY RULES (Intelligence Engine) ---
class CategoryRule(Base):
    """
    This model stores the rules created by Developer 1.
    It maps a 'pattern' found in descriptions to a specific 'category'.
    """
    __tablename__ = "category_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    pattern = Column(String, nullable=False)        # e.g., 'Starbucks'
    category = Column(String, nullable=False)       # e.g., 'Food & Dining'
    match_type = Column(String, default="keyword")  # e.g., 'keyword' or 'exact'
    user_id = Column(Integer, ForeignKey("users.id"))
=======
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    amount = Column(Float, nullable=False)
    description = Column(String)
    transaction_type = Column(String) 
    category = Column(String)
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
>>>>>>> cb8739c9cc3aa7a178da3c1967b6e0798d062a28
