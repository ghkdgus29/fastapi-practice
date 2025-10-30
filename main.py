from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import AfterValidator

app = FastAPI()


def check_item_id(item_id: int) -> int:
    if item_id > 1000:
        raise ValueError("Item ID must be less than 1000")
    return item_id


@app.get("/items2/{item_id}")
async def read_items2(
    item_id: Annotated[int, AfterValidator(check_item_id)],
    q: str | None = None,
    size: Annotated[float, Query(gt=0, lt=1.0)] = 0.5,
):
    results = {"item_id": item_id, "size": size}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
    q: str | None = None,
    size: Annotated[float, Query(gt=0, lt=1.0)] = 0.5,
):
    results = {"item_id": item_id, "size": size}
    if q:
        results.update({"q": q})
    return results
