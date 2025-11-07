from typing import Any

import orjson
from fastapi import FastAPI, Response
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    ORJSONResponse,
    PlainTextResponse,
    RedirectResponse,
    StreamingResponse,
)

app = FastAPI()


@app.get("/items/", response_class=ORJSONResponse)
async def read_items():
    return ORJSONResponse([{"items": "Foo"}])


@app.get("/items2/")
async def read_items2():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """

    return HTMLResponse(content=html_content, status_code=200)


@app.get("/legacy/")
def get_legacy_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")


@app.get("/", response_class=PlainTextResponse)
async def main():
    return "Hello, World!"


@app.get("/typer")
async def redirct_typer():
    return RedirectResponse("https://typer.tiangolo.com/")


@app.get("/pydantic", response_class=RedirectResponse, status_code=302)
async def redirect_pydantic():
    return "https://docs.pydantic.dev/"


async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"


@app.get("/stream")
async def stream_video():
    return StreamingResponse(fake_video_streamer())


@app.get("/file", response_class=FileResponse)
async def read_file():
    return FileResponse("log.txt")


class CustomORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed to use this response class"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)


@app.get("/custom-orjson", response_class=CustomORJSONResponse)
async def custom_orjson():
    return {"message": "Hello, World!"}
