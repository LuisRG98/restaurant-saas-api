from fastapi import FastAPI
from app.api.restaurants import router as restaurants_router


from app.core.exceptions import (
    RestaurantAlreadyExistsError,
    RestaurantNotFoundError,
)
from app.core.exception_handlers import (
    restaurant_already_exists_handler,
    restaurant_not_found_handler,
)

app = FastAPI(
    title="Restaurant Management API",
    description="Backend API for restaurant management",
    version="1.0.0",
)


app.add_exception_handler(
    RestaurantNotFoundError,
    restaurant_not_found_handler,
)

app.add_exception_handler(
    RestaurantAlreadyExistsError,
    restaurant_already_exists_handler,
)

app.include_router(restaurants_router)


@app.get("/api/v1/health")
def health_check():
    return {
    "status": "healthy",
    "service": "restaurant-api",
    "version": "1.0.0"
    }