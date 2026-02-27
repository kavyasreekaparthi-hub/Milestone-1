from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    # Primary Key: A unique ID for every user
    id = Column(Integer, primary_key=True, index=True)
    
    # User Details
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # We store the 'hash' of the password, never the plain text
    password_hash = Column(String, nullable=False)
    
    phone = Column(String, nullable=True)
    kyc_status = Column(String, default="unverified") # e.g., verified, pending
    
    # Automatically track when the user joined
    created_at = Column(DateTime(timezone=True), server_default=func.now())