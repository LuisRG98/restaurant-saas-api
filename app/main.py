from fastapi import FastAPI


app = FastAPI(
    title="Restaurant Management API",
    description="Backend API for restaurant management",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/api/v1/health")
def health_check():
    return {
    "status": "healthy",
    "service": "restaurant-api",
    "version": "1.0.0"
    }