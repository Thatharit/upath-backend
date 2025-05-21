from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import models, database
from app.schemas import job_schema  # เปลี่ยนชื่อ schema

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=job_schema.Job)
def create_job(job: job_schema.JobCreate, db: Session = Depends(get_db)):
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/", response_model=list[job_schema.Job])
def read_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()
