from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(
    q: str | None = None, skip: int = 0, limit: int = 100
) -> dict:
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


CommonsDep = Annotated[dict, Depends(common_parameters)]


@app.get("/items2/")
async def read_items2(commons: CommonsDep):
    return commons


@app.get("/users2/")
async def read_users2(commons: CommonsDep):
    return commons
