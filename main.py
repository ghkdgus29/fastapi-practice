from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: Annotated[str, Field(examples=["Foo"])]
    description: Annotated[str | None, Field(examples=["A very nice item"])]
    price: Annotated[float, Field(examples=[42.0])]
    tax: Annotated[float | None, Field(examples=[3.2])] = None

    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "name": "Foo",
    #                 "description": "The Foo fighters",
    #                 "price": 42.0,
    #                 "tax": 3.2,
    #             }
    #         ]
    #     }
    # }


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}


class Item2(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items2/{item_id}")
async def update_item2(
    item_id: int,
    item: Annotated[
        Item2,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal item",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice item",
                        "price": 42.0,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An item with converted data",
                    "description": "An item with `converted` data works `correctly.`",
                    "value": {
                        "name": "Bar",
                        "price": "42.0",
                    },
                },
                "invalid": {
                    "summary": "An invalid item",
                    "value": {
                        "name": "Baz",
                        "price": "forty-two",
                    },
                },
            },
        ),
    ],
):
    return {"item_id": item_id, "item": item}
