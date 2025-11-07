from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the darkside, we have cookies"}


@app.post("/cookie/")
def create_cookie2():
    content = {"message": "Come to the darkside, we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return response
