from fastapi import FastAPI

app = FastAPI(
    title="AptiQuest API",
    description="Backend API for AptiQuest",
    version="1.0.0"
)


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