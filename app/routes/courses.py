from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import models, database
from app.schemas import course_schema
from datetime import datetime

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=course_schema.Course)
def create_course(course: course_schema.CourseCreate, db: Session = Depends(get_db)):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/", response_model=list[course_schema.Course])
def read_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()
@router.post("/enroll")
async def enroll_course(user_id: int, course_id: int):
    query = models.enrollments.insert().values(
        user_id=user_id,
        course_id=course_id,
        status="pending",
        enrolled_at=datetime.utcnow()
    )
    last_record_id = await database.database.execute(query)
    return {"message": "Enrollment created", "enrollment_id": last_record_id}

@router.post("/enroll/cancel")
async def cancel_enrollment(user_id: int, enrollment_id: int):
    # ตรวจสอบว่า enrollment นี้เป็นของ user จริงไหม
    query = select(models.Enrollment).where(
        models.Enrollment.id == enrollment_id,
        models.Enrollment.user_id == user_id
    )
    result = await database.fetch_one(query)

    if not result:
        raise HTTPException(status_code=404, detail="Enrollment not found or unauthorized")

    if result.status in ["completed", "cancelled"]:
        raise HTTPException(status_code=400, detail=f"Cannot cancel a {result.status} enrollment.")

    # อัปเดตสถานะเป็น cancelled
    update_query = (
        update(models.Enrollment)
        .where(models.Enrollment.id == enrollment_id)
        .values(status="cancelled")
    )
    await database.execute(update_query)

    return {"message": "Enrollment cancelled successfully"}

