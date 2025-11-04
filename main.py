from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()

fake_db = {}


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"title": "Foo", "description": "The Foo fighters", "price": 42.0},
    "bar": {
        "title": "Bar",
        "description": "The Bar fighters",
        "price": 42.0,
        "tax": 20.2,
    },
    "baz": {
        "title": "Baz",
        "description": None,
        "price": 42.0,
        "tax": 10.5,
        "tags": [],
    },
}


@app.get("/items/{item_id}")
async def read_item(item_id: str) -> Item:
    return items[item_id]


@app.put("/items/{item_id}")
async def replace_item(item_id: str, item: Item) -> Item:
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded


@app.patch("/items/{item_id}")
async def update_item(item_id: str, item: Item) -> Item:
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item_model.model_copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item
