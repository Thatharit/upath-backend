# app/core/skill_analysis.py

from app.data.skill_data import career_skills

def analyze_skill_gap(current_skills: list[str], target_career: str) -> list[str]:
    required_skills = career_skills.get(target_career, [])
    missing_skills = [skill for skill in required_skills if skill not in current_skills]
    return missing_skills
