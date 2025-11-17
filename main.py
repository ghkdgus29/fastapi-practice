import gzip
import time
from typing import Annotated, Callable

from fastapi import APIRouter, Body, FastAPI, HTTPException, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from starlette.requests import Request


class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body


class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler


app = FastAPI()
app.router.route_class = GzipRoute


@app.post("/sum")
async def sum_numbers(numbers: Annotated[list[int], Body()]):
    return {"sum": sum(numbers)}


class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler


app2 = FastAPI()
app2.router.route_class = ValidationErrorLoggingRoute

app.mount("/app2", app2)


@app2.post("/")
async def sum_numbers2(numbers: Annotated[list[int], Body()]):
    return sum(numbers)


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler


app3 = FastAPI()
router = APIRouter(route_class=TimedRoute)

app.mount("/app3", app3)


@app3.get("/")
async def not_timed():
    return {"message": "Not timed"}


@router.get("/timed")
async def timed():
    return {"message": "It's the time of my life"}


app3.include_router(router)
