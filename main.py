from typing import Any
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "portal gun", "price": 100.0},
        {"name": "jetpack", "price": 150.0},
    ]


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True


@app.post("/users/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn2(BaseUser):
    password: str


@app.post("/users2/", response_model=BaseUser)
async def create_user2(user: UserIn2) -> BaseUser:
    return user


@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})


@app.get("/portal2", response_model=None)
async def get_portal2(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}


class Item2(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model_exclude_unset=True)
async def read_item2(item_id: str) -> Item2:
    return items[item_id]


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str) -> Item:
    return items[item_id]


@app.get(
    "/items/{item_id}/public",
    response_model=Item,
    response_model_exclude={"tax"},
)
async def read_item_public(item_id: str) -> Item:
    return items[item_id]
