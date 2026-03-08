<<<<<<< HEAD
import re
from fastapi import HTTPException

def validate_email_format(email: str):
    """Ensures the email follows a standard pattern."""
    email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(email_regex, email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    return email

def validate_phone_number(phone: str):
    """Ensures phone number is 10-15 digits long."""
    if not (10 <= len(phone) <= 15 and phone.isdigit()):
        raise HTTPException(status_code=400, detail="Invalid phone number")
    return phone

def validate_positive_amount(amount: float):
    """Ensures transaction or balance amounts are not negative."""
    if amount < 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
=======
import re
from fastapi import HTTPException

def validate_email_format(email: str):
    """Ensures the email follows a standard pattern."""
    email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(email_regex, email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    return email

def validate_phone_number(phone: str):
    """Ensures phone number is 10-15 digits long."""
    if not (10 <= len(phone) <= 15 and phone.isdigit()):
        raise HTTPException(status_code=400, detail="Invalid phone number")
    return phone

def validate_positive_amount(amount: float):
    """Ensures transaction or balance amounts are not negative."""
    if amount < 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
>>>>>>> cb8739c9cc3aa7a178da3c1967b6e0798d062a28
    return amount