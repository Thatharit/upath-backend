from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.db import models, database
from app.schemas import career_schema

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/recommend", response_model=List[career_schema.Career])
def recommend_careers(skills: str = Query(..., description="Comma separated skills"),
                      db: Session = Depends(get_db)):
    input_skills = set(skill.strip().lower() for skill in skills.split(","))
    careers = db.query(models.Career).all()

    def score(career):
        career_skills = set(s.strip().lower() for s in career.skill_tags.split(",") if career.skill_tags)
        return len(input_skills.intersection(career_skills))

    # เลือกอาชีพที่มีคะแนนตรงกันมากกว่า 0 แล้วเรียงตามคะแนน
    recommended = [c for c in careers if score(c) > 0]
    recommended.sort(key=score, reverse=True)

    return recommended
@router.get("/careers/skill-gap")
async def skill_gap(career_name: str, user_skills: str):
    user_skill_set = set([s.strip().lower() for s in user_skills.split(",")])

    # ดึงข้อมูลอาชีพจากฐานข้อมูล
    query = models.careers.select().where(models.careers.c.name == career_name)
    career = await database.database.fetch_one(query)

    if not career:
        return {"error": "Career not found"}

    required_skills = set([s.strip().lower() for s in career["skill_tags"].split(",")])
    missing_skills = list(required_skills - user_skill_set)

    return {
        "career": career_name,
        "you_have": list(user_skill_set),
        "required": list(required_skills),
        "should_learn": missing_skills,
    }

