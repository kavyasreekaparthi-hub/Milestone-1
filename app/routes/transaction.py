from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import transaction as schemas
from app.services import transaction_service as service

router = APIRouter(
    prefix="/api/transactions",
    tags=["transactions"]
)

# Endpoint to List Transactions with filters
@router.get("/", response_model=List[schemas.Transaction])
def read_transactions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    transactions = service.get_transactions(db, skip=skip, limit=limit)
    return transactions

# Endpoint to Import CSV
@router.post("/import")
async def import_transactions(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    return await service.handle_csv_upload(db, file)