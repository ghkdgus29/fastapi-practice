import random
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import AfterValidator

app = FastAPI()


@app.get("/items/")
async def read_items(
    q: Annotated[
        list[str] | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            alias="item-query",
            deprecated=True,
            min_length=3,
        ),
    ] = None,
    hidden_query: Annotated[str, Query(include_in_schema=False)] = None,
) -> dict:
    return {"items": q, "hidden_query": hidden_query}


data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError("Invalid ID, it must start with 'isbn-' or 'imdb-'")
    return id


@app.get("/books")
async def read_books(id: Annotated[str | None, AfterValidator(check_valid_id)] = None):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "item": item}
