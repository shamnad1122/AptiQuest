from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.controllers.auth_controller import router as auth_router
from app.controllers.question_controller import router as question_router, topics_router
from app.controllers.user_controller import router as user_router

app = FastAPI(
    title="AptiQuest API",
    description="Backend API for AptiQuest",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(question_router)
app.include_router(topics_router)


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
