from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return {"offer": offer}


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return {"images": images}


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return {"weights": weights}
