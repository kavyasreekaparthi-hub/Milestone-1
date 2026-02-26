from sqlalchemy import create_engine  # Remove create_all from here
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ... rest of your code ...
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/banking_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# This is the get_db function your main.py was looking for
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()