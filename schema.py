from pydantic import BaseModel, Field
from datetime import datetime


class Pagination(BaseModel):
    limit: int = Field(gt=0, default=10)
    page: int = Field(ge=0, default=0)


class Items(BaseModel):
    name: str
    category: str
    manufacturer: str
    item_code: int = Field(gt=0)
    description: str
    price: int = Field(gt=0)  # int имеется в виду считая от копеек т.е. - 1 р. тут будет равен 100
    quantity: int = Field(ge=0)


class AddItems(Items):
    category: str = "all"
    manufacturer: str = "Unknown"
    description: str = "No description"


class PutItems(Items):
    published: bool


class PatchItems(PutItems):
    name: str | None = None
    category: str | None = None
    manufacturer: str | None = None
    item_code: int | None = Field(gt=0, default=None)
    description: str | None = None
    price: int | None = Field(gt=0, default=None)
    quantity: int | None = Field(gt=0, default=None)
    published: bool | None = None


class GetItems(PutItems):
    id: int
    time_create: datetime
