from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    RestaurantAlreadyExistsError,
    RestaurantNotFoundError,
)


async def restaurant_not_found_handler(
    request: Request,
    exc: RestaurantNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "RESTAURANT_NOT_FOUND",
                "message": str(exc),
            }
        },
    )


async def restaurant_already_exists_handler(
    request: Request,
    exc: RestaurantAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={
            "error": {
                "code": "RESTAURANT_ALREADY_EXISTS",
                "message": str(exc),
            }
        },
    )