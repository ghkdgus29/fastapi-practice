from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(
    user_agent: Annotated[str | None, Header()] = None,
    strange_header: Annotated[str | None, Header(convert_underscores=False)] = None,
    x_token: Annotated[list[str] | None, Header()] = None,
):
    return {
        "User-Agent": user_agent,
        "strange_header": strange_header,
        "x_token": x_token,
    }
