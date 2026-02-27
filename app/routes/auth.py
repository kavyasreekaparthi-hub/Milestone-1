from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, utils
from app.utils import security  # <--- Make sure this line is here!
from app.schemas import user as user_schemas
from app.schemas import auth as auth_schemas
from app.dependencies import get_db

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Note: We changed 'schemas.user.UserOut' to 'user_schemas.UserOut'
@router.post("/signup", response_model=user_schemas.UserOut)
def signup(user_data: user_schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Check if user exists
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. HASH THE PASSWORD (This is where the code goes!)
    hashed_password = security.get_password_hash(user_data.password)
    
    # 3. Create user
    new_user = models.User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password,
        phone=user_data.phone
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Note: We changed 'schemas.auth.Token' to 'auth_schemas.Token'
@router.post("/login", response_model=auth_schemas.Token)
def login(user_credentials: user_schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    # Use security.verify_password here!
    if not user or not security.verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}