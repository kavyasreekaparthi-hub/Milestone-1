<<<<<<< HEAD
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
=======
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
>>>>>>> cb8739c9cc3aa7a178da3c1967b6e0798d062a28
    email: str | None = None