# app/schemas/job_schema.py
from pydantic import BaseModel
from typing import List

class JobBase(BaseModel):
    title: str
    company: str
    location: str
    required_skills: List[str]

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int

    class Config:
        orm_mode = True
