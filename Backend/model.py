from pydantic import BaseModel, EmailStr
from typing import Optional

class Kmeans(BaseModel):
    CLIENT_AGE:int
    CLIENT_ENCOURS_ENGAGEMENT: float
    CLIENT_MMM: float
    CLIENT_NOMBRE_CARTES: int
    CLIENT_VRD_MOY: float
    TOTAL_PACK:float

class User(BaseModel):
    company: str
    email: EmailStr
    password: str
    otp: int
    verified: bool
class Login(BaseModel):
    email: EmailStr
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    email :Optional[EmailStr] = None



