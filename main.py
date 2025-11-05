import time
from typing import Annotated

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"query_or_default": query_or_default}


def get_timestamp() -> float:
    ts = time.time()
    print(f"get_timestamp: {ts}")
    return ts


@app.get("/cached")
def read_cached(
    a: Annotated[float, Depends(get_timestamp)],
    b: Annotated[float, Depends(get_timestamp)],
):
    return {"a": a, "b": b}


@app.get("/no-cache")
def read_no_cache(
    a: Annotated[float, Depends(get_timestamp)],
    b: Annotated[float, Depends(get_timestamp, use_cache=False)],
):
    return {"a": a, "b": b}
