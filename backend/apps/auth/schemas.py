from pydantic import BaseModel
from datetime import datetime

class LoginRequest(BaseModel):
    matricule: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    matricule: str
    role : str
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True