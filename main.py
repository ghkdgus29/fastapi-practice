from fastapi import FastAPI

# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()


# app.add_middleware(HTTPSRedirectMiddleware)  # http -> https / ws -> wss redirect
# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=[
#         "example.com",
#         "*.example.com",
#     ],
# )  # allowed hosts to access the server
app.add_middleware(
    GZipMiddleware, minimum_size=1000, compresslevel=5
)  # if request includes Accept-Encoding: gzip, then gzip the response


@app.get("/")
async def main():
    return {"message": "Hello World"}
