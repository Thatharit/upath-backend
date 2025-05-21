from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    name: str
    interests: List[str]
    favorite_subjects: List[str]

class UserCreate(UserBase):
    password: str  # ✅ เพิ่ม password ที่นี่

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class LoginSchema(BaseModel):
    username: str  # ✅ หรือใช้ name: str ก็ได้ ถ้าไม่ใช้ OAuth2
    password: str
