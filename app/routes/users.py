# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import user_schema
from app.db import models, database
from app.routes.auth_helper import get_current_user

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=list[user_schema.User])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get("/me", response_model=user_schema.User)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user
