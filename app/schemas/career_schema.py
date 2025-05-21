# app/schemas/career_schema.py
from pydantic import BaseModel
from typing import List

class CareerBase(BaseModel):
    name: str
    description: str
    required_skills: List[str]

class CareerCreate(CareerBase):
    pass

class Career(CareerBase):
    id: int

    class Config:
        orm_mode = True
