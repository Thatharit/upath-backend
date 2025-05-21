from fastapi import APIRouter
from app.services.external_api import fetch_thaimooc_courses

router = APIRouter()

@router.get("/external/thaimooc")
async def get_thaimooc_courses():
    return await fetch_thaimooc_courses()