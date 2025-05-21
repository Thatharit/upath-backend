# app/routes/skillgap.py

from fastapi import APIRouter
from pydantic import BaseModel
from app.core.skill_analysis import analyze_skill_gap

router = APIRouter()

class SkillGapRequest(BaseModel):
    current_skills: list[str]
    target_career: str

class SkillGapResponse(BaseModel):
    missing_skills: list[str]

@router.post("/skill-gap", response_model=SkillGapResponse)
def skill_gap_analysis(request: SkillGapRequest):
    result = analyze_skill_gap(request.current_skills, request.target_career)
    return {"missing_skills": result}
