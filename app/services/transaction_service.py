<<<<<<< HEAD
import csv
import io
from sqlalchemy.orm import Session
from app.models.transaction import Transaction

async def handle_csv_upload(db: Session, file, account_id: int):
    contents = await file.read()
    decoded = contents.decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded))
    
    transactions = []
    for row in reader:
        new_txn = Transaction(
            account_id=account_id,
            description=row['description'],
            amount=float(row['amount']),
            category=row['category'],
            txn_date=row['date']
        )
        db.add(new_txn)
        transactions.append(new_txn)
    
    db.commit()
=======
import csv
import io
from sqlalchemy.orm import Session
from app.models.transaction import Transaction

async def handle_csv_upload(db: Session, file, account_id: int):
    contents = await file.read()
    decoded = contents.decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded))
    
    transactions = []
    for row in reader:
        new_txn = Transaction(
            account_id=account_id,
            description=row['description'],
            amount=float(row['amount']),
            category=row['category'],
            txn_date=row['date']
        )
        db.add(new_txn)
        transactions.append(new_txn)
    
    db.commit()
>>>>>>> cb8739c9cc3aa7a178da3c1967b6e0798d062a28
    return {"message": f"Successfully imported {len(transactions)} transactions"}