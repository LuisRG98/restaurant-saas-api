from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_db
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse,
    RestaurantUpdate
)
from app.services.restaurant import RestaurantService


router = APIRouter(
    prefix="/api/v1/restaurants",
    tags=["Restaurants"],
)

@router.get(
        "/",
        response_model=list[RestaurantResponse],
    )
def get_restaurants(
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    return service.get_all()


@router.post(
    "/",
    response_model=RestaurantResponse,
    status_code=status.HTTP_201_CREATED,
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

    return service.get_restaurant(restaurant_id)


@router.patch(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def update_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    return service.update_restaurant(
        restaurant_id,
        restaurant_data,
    )


@router.delete(
    "/{restaurant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    service = RestaurantService(db)

    service.delete_restaurant(restaurant_id)

    return None