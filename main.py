from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()

data = {
    "plumbus": {"description": "Freshly picked plumbus", "owner": "Morty"},
    "portal-gun": {"description": "A gun that shoots portals", "owner": "Rick"},
}


class OwnerError(Exception):
    pass


def get_username():
    try:
        print("generate username")
        yield "Rick"
        print("username generated")
    except OwnerError as e:
        print("owner error")
        raise HTTPException(status_code=400, detail=f"Owner error: {e}")


@app.get("/items/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    item = data[item_id]
    if item["owner"] != username:
        raise OwnerError(f"User {username} is not the owner of item {item_id}")
    return item


def get_username2():
    try:
        yield "Rick"
    except OwnerError:
        print("Oops, we didn't raise again, Britney")
        raise


@app.get("/items2/{item_id}")
def get_item2(item_id: str, username: Annotated[str, Depends(get_username2)]):
    if item_id == "portal-gun":
        raise OwnerError("Portal gun is not allowed")
    if item_id != "plumbus":
        raise HTTPException(status_code=404, detail="Item not found")
    return item_id


def get_username3():
    try:
        yield "Rick"
    finally:
        print("Clean up before response is sent")


@app.get("/users/me")
def get_user_me(username: Annotated[str, Depends(get_username3, scope="function")]):
    return {"username": username}


def a_dep():
    try:
        print("a_dep")
        yield "dep_a"
    finally:
        print("a_dep end")


def b_dep(dep_a: Annotated[str, Depends(a_dep)]):
    print(f"b_dep received dep_a: {dep_a}")
    try:
        print("b_dep")
        yield "dep_b"
    finally:
        print("b_dep end")


def c_dep(dep_b: Annotated[str, Depends(b_dep)]):
    print(f"c_dep received dep_b: {dep_b}")
    try:
        print("c_dep")
        yield "dep_c"
    finally:
        print("c_dep end")


@app.get("/order/")
def get_order(dep_c: Annotated[str, Depends(c_dep)]):
    return "ok"
