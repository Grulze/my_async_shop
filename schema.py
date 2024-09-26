from pydantic import BaseModel, Field
from datetime import datetime


class Pagination(BaseModel):
    limit: int = Field(gt=0)
    page: int = Field(ge=0)


class Items(BaseModel):
    name: str
    category: str
    manufacturer: str
    article: int
    description: str
    price: int  # int имеется в виду считая от копеек т.е. - 1 р. тут будет равен 100
    quantity: int


class AddItems(Items):
    category: str = "all"
    manufacturer: str = "Unknown"
    description: str = "No description"
    quantity: int = 1


class PutItems(Items):
    published: bool


class PatchItems(PutItems):
    name: str | None = None
    category: str | None = None
    manufacturer: str | None = None
    article: int | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    published: bool | None = None


class GetItems(PutItems):
    id: int
    time_create: datetime
