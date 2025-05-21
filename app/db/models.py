# app/db/models.py
from sqlalchemy import Column, Integer, String, Text, JSON, Table, ForeignKey, DateTime
from app.db.database import Base
from datetime import datetime
from sqlalchemy import Float

# User Model (เดิม)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    interests = Column(JSON)
    favorite_subjects = Column(JSON)

# Career Model
class Career(Base):
    __tablename__ = "careers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    skill_tags = Column(String)

# Course Model
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    provider = Column(String)
    tags = Column(JSON)
    description = Column(Text)

# Job Model
class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String)
    location = Column(String)
    required_skills = Column(JSON)

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    status = Column(String)  # เช่น pending, paid, completed
    enrolled_at = Column(DateTime, default=datetime.utcnow)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"))
    amount = Column(Float)
    status = Column(String)  # เช่น success, failed
    paid_at = Column(DateTime, default=datetime.utcnow)

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    rating = Column(Integer)  # 1 ถึง 5
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)



