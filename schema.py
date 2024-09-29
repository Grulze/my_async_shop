from pydantic import BaseModel, Field
from datetime import datetime


class Pagination(BaseModel):
    limit: int = Field(gt=0, default=10)
    page: int = Field(ge=0, default=0)


class Items(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    category: str = Field(min_length=3, max_length=30)
    manufacturer: str = Field(min_length=3, max_length=30)
    item_code: int = Field(gt=0)
    description: str = Field(min_length=10, max_length=400)
    price: int = Field(gt=0)  # int имеется в виду считая от копеек т.е. - 1 р. тут будет равен 100
    quantity: int = Field(ge=0)


class AddItems(Items):
    category: str = Field(min_length=3, max_length=30, default="all")
    manufacturer: str = Field(min_length=3, max_length=30, default="Unknown")
    description: str = Field(min_length=10, max_length=400, default="No description")


class PutItems(Items):
    published: bool


class PatchItems(PutItems):
    name: str | None = Field(min_length=3, max_length=50, default=None)
    category: str | None = Field(min_length=3, max_length=30, default=None)
    manufacturer: str | None = Field(min_length=3, max_length=30, default=None)
    item_code: int | None = Field(gt=0, default=None)
    description: str | None = Field(min_length=10, max_length=400, default=None)
    price: int | None = Field(gt=0, default=None)
    quantity: int | None = Field(gt=0, default=None)
    published: bool | None = None


class GetItems(PutItems):
    id: int
    time_create: datetime
