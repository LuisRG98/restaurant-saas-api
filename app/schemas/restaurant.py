from pydantic import BaseModel, Field


class RestaurantBase(BaseModel):
    name: str
    address: str
    phone: str

    
class RestaurantCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=100
    )

    address: str = Field(
        min_length=5,
        max_length=255
    )

    phone: str = Field(
        min_length=7,
        max_length=30
    )


class RestaurantUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    address: str | None = Field(
        default=None,
        min_length=5,
        max_length=255
    )

    phone: str | None = Field(
        default=None,
        min_length=7,
        max_length=30
    )


class RestaurantResponse(BaseModel):
    id: int
    name: str
    address: str
    phone: str

    model_config = {
        "from_attributes": True
    }