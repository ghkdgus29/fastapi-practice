from enum import Enum

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


class Tags(Enum):
    items = "items"
    users = "users"


@app.post(
    "/items/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create an item",
    response_description="The created item",
    deprecated=True,
)
async def create_item(item: Item):
    """
    Create an item with all the information

    - **name**: The name of the item
    - **description**: The description of the item
    - **price**: The price of the item
    - **tax**: The tax of the item
    - **tags**: The tags of the item
    """
    return item


@app.get("/items2/", tags=[Tags.items])
async def create_item2(item: Item) -> Item:
    return item


@app.get("/items3/", tags=[Tags.items])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=[Tags.users])
async def read_users():
    return [{"username": "johndoe"}]
