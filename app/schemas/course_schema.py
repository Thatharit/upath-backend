# app/schemas/course_schema.py
from pydantic import BaseModel
from typing import List

class CourseBase(BaseModel):
    title: str
    provider: str
    tags: List[str]
    description: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

    class Config:
        orm_mode = True
