from fastapi import FastAPI

from app.controllers.auth_controller import router as auth_router
from app.controllers.user_controller import router as user_router
app = FastAPI(
    title="AptiQuest API",
    description="Backend API for AptiQuest",
    version="1.0.0"
)


app.include_router(user_router)
app.include_router(auth_router)
@app.get("/")
def root():
    return {
        "message": "Welcome to AptiQuest API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }