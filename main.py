from app.routes import users, careers, courses, jobs, payments, reviews, auth, skillgap, external
from app.db.database import Base, engine
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users")
app.include_router(careers.router, prefix="/careers")
app.include_router(courses.router, prefix="/courses")
app.include_router(jobs.router, prefix="/jobs")
app.include_router(payments.router, prefix="/api")
app.include_router(reviews.router, prefix="/api")
app.include_router(auth.router, prefix="/auth")
app.include_router(skillgap.router)
app.include_router(external.router, prefix="/api")