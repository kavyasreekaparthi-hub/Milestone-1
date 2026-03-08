from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import io
from typing import List

# Internal project imports
from app.database import engine, Base, get_db
from app.models import Transaction, User, Account, CategoryRule, Budget
from app.routes import auth
from app.services.categorizer import auto_categorize
from app.services.budget_service import calculate_spent_amount

# 1. Database Initialization
# This ensures all tables (Transactions, Rules, Budgets) are created in PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Modern Digital Banking API")

# 2. Authentication Routes
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Banking API is running successfully!"}

# --- SECTION: TRANSACTION INGESTION (Week 2/3) ---

@app.post("/api/transactions/upload/{account_id}", tags=["Transactions"])
async def upload_transactions(
    account_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        acc_info = db.query(Account).filter(Account.id == account_id).first()
        if not acc_info:
            raise HTTPException(status_code=404, detail="Account not found")
        
        user_id = acc_info.user_id

        for _, row in df.iterrows():
            new_tx = Transaction(
                account_id=account_id,
                amount=row['amount'],
                description=row['description'],
                transaction_type=row['transaction_type'],
                category=row.get('category', 'Uncategorized')
            )
            db.add(new_tx)
            db.flush() 

            # Trigger logic engine to auto-tag categories
            auto_categorize(db, new_tx, user_id)
        
        db.commit()
        return {"status": "success", "message": f"Imported {len(df)} transactions and applied rules"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# --- SECTION: CATEGORIZATION ENGINE (Week 3) ---

@app.post("/api/categories/rules", tags=["Categories"])
def create_rule(user_id: int, category: str, keyword: str, db: Session = Depends(get_db)):
    new_rule = CategoryRule(user_id=user_id, category=category, keyword_pattern=keyword)
    db.add(new_rule)
    db.commit()
    return {"message": f"Rule created: '{keyword}' matches will be tagged as '{category}'"}

@app.post("/api/transactions/cleanup/{account_id}", tags=["Categories"])
def cleanup_transactions(account_id: int, db: Session = Depends(get_db)):
    acc = db.query(Account).filter(Account.id == account_id).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    
    user_id = acc.user_id
    transactions = db.query(Transaction).filter(Transaction.account_id == account_id).all()
    
    count = 0
    for tx in transactions:
        if tx.category in ["Uncategorized", "Pending", "", None]:
            auto_categorize(db, tx, user_id)
            count += 1
            
    return {"message": f"Processed {count} transactions using current rules"}

@app.put("/api/transactions/{transaction_id}/category", tags=["Categories"])
def update_transaction_category(transaction_id: int, new_category: str, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    transaction.category = new_category
    db.commit()
    return {"message": f"Transaction {transaction_id} updated to {new_category}"}

@app.post("/api/transactions/bulk-categorize", tags=["Categories"])
def bulk_categorize(transaction_ids: List[int], category: str, db: Session = Depends(get_db)):
    db.query(Transaction).filter(Transaction.id.in_(transaction_ids)).update(
        {"category": category}, synchronize_session=False
    )
    db.commit()
    return {"message": f"Updated {len(transaction_ids)} transactions to {category}"}

# --- SECTION: BUDGETS (Milestone 2: Week 4) ---

@app.post("/api/budgets", tags=["Budgets"])
def create_budget(user_id: int, category: str, limit: float, month: int, year: int, db: Session = Depends(get_db)):
    new_budget = Budget(user_id=user_id, category=category, limit_amount=limit, month=month, year=year)
    db.add(new_budget)
    db.commit()
    return {"message": f"Budget of {limit} created for {category} in {month}/{year}"}

@app.get("/api/budgets/{user_id}/progress", tags=["Budgets"])
def get_budget_progress(user_id: int, month: int, year: int, db: Session = Depends(get_db)):
    budgets = db.query(Budget).filter(Budget.user_id == user_id, Budget.month == month, Budget.year == year).all()
    
    progress_report = []
    for b in budgets:
        spent = calculate_spent_amount(db, user_id, b.category, month, year)
        remaining = b.limit_amount - spent
        percentage = (spent / b.limit_amount * 100) if b.limit_amount > 0 else 0
        
        progress_report.append({
            "category": b.category,
            "limit": b.limit_amount,
            "spent": spent,
            "remaining": max(0, remaining),
            "percentage_used": round(percentage, 2),
            "status": "Exceeded" if spent > b.limit_amount else "On Track"
        })
    return progress_report