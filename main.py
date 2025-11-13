from fastapi import FastAPI
from fastapi.requests import Request

app = FastAPI()


@app.get("/items/{item_id}")
def read_root(item_id: str, request: Request):
    client_host = request.client.host
    return {"item_id": item_id, "client_host": client_host}
