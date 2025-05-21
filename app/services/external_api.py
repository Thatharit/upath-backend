import httpx

THAIMOOC_API_URL = "https://thaimooc.org/api/courses"  # (เปลี่ยน URL จริงได้)

async def fetch_thaimooc_courses():
    async with httpx.AsyncClient() as client:
        response = await client.get(THAIMOOC_API_URL)
        if response.status_code == 200:
            return response.json()
        return {"error": "Failed to fetch ThaiMOOC data"}