from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_db
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse,
)
from app.services.restaurant import RestaurantService


router = APIRouter(
    prefix="/api/v1/restaurants",
    tags=["Restaurants"],
)

@router.get("/")
def get_restaurants(
    db: Session = Depends(get_db),
):
    return {
        "message": "Database session received"
    }


@router.get("/database-check")
def database_check(
    db: Session = Depends(get_db),
):
    result = db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }


@router.post(
    "/",
    response_model=RestaurantResponse,
    status_code=201,
)
def create_restaurant(
    data: RestaurantCreate,
    db: Session = Depends(get_db),
):

    service = RestaurantService(db)

    return service.create(data)


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):

    service = RestaurantService(db)

    return service.get_by_id(restaurant_id)