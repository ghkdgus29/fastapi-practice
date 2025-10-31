from typing import Annotated

from fastapi import Body, FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items0/{item_id}")
async def update_item0(item_id: Annotated[int, Path(ge=0, le=1000)], item: Item):
    return {"item_id": item_id, "item": item}


@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(ge=0, le=1000)], item: Item, user: User
):
    return {"item_id": item_id, "item": item, "user": user}


@app.put("/items2/{item_id}")
async def update_item2(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body(gt=0)]
):
    return {"item_id": item_id, "item": item, "user": user, "importance": importance}


@app.put("/items3/{item_id}")
async def update_item3(item_id: int, item: Annotated[Item, Body(embed=True)]):
    return {"item_id": item_id, "item": item}
