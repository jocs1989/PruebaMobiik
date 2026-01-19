from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None

    class Config:
        orm_mode = True
