from fastapi import FastAPI, status

app = FastAPI()


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str) -> dict:
    return {"name": name, "message": "Item created successfully"}
