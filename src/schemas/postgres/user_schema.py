from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: str
    roles: List[str] = ["user"]

class UserRead(BaseModel):
    id: int
    username: str
    email: Optional[str]
    full_name: Optional[str]
    disabled: bool
    roles: List[str]

    class Config:
        from_attributes = True
