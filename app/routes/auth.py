from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import models, database
from app.schemas import user_schema
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter()

SECRET_KEY = "your-secret-key"  # 👉 ควรเก็บใน .env จริง ๆ
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=user_schema.User)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter_by(name=user.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed = hash_password(user.password)
    db_user = models.User(name=user.name, password=hashed,
                          interests=user.interests, favorite_subjects=user.favorite_subjects)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(form_data: user_schema.LoginSchema, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(name=form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": user.name})
    return {"access_token": token, "token_type": "bearer"}
