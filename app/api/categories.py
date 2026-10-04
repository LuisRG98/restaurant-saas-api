from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_role,
)
from app.models.user import User
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category_service import CategoryService


router = APIRouter(
    prefix="/api/v1/categories",
    tags=["Categories"],
)


@router.get(
    "/",
    response_model=list[CategoryResponse],
)
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    service = CategoryService(db)

    return service.get_all(current_user)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ADMIN", "MANAGER")
    ),
):
    service = CategoryService(db)

    return service.create(
        category_data,
        current_user,
    )


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    service = CategoryService(db)

    return service.get_by_id(
        category_id,
        current_user,
    )


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ADMIN", "MANAGER")
    ),
):
    service = CategoryService(db)

    return service.update(
        category_id,
        category_data,
        current_user,
    )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ADMIN", "MANAGER")
    ),
):
    service = CategoryService(db)

    service.delete(
        category_id,
        current_user,
    )

    return None