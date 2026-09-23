from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.restaurants import router as restaurants_router
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.core.exceptions import AppException


app = FastAPI(
    title="Restaurant Management API",
    description="Backend API for restaurant management",
    version="1.0.0",
)

@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
        },
    )

app.include_router(restaurants_router)
app.include_router(auth_router)
app.include_router(users_router)


@app.get("/api/v1/health")
def health_check():
    return {
    "status": "healthy",
    "service": "restaurant-api",
    "version": "1.0.0"
    }