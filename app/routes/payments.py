from fastapi import APIRouter
from datetime import datetime
from app.db import database
from app.db import models

router = APIRouter()

@router.post("/payment")
async def process_payment(user_id: int, enrollment_id: int, amount: float):
    # เพิ่มข้อมูลการชำระเงิน
    query = models.payments.insert().values(
        user_id=user_id,
        enrollment_id=enrollment_id,
        amount=amount,
        status="success",
        paid_at=datetime.utcnow()
    )
    await database.execute(query)

    # อัปเดตสถานะ enrollment ให้เป็น "paid"
    update_query = models.enrollments.update().where(
        models.enrollments.c.id == enrollment_id
    ).values(status="paid")
    await database.execute(update_query)

    return {"message": "Payment successful"}
