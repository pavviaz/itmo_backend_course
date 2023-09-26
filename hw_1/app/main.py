import time

from app.router import router as main_router
from app.shop.router import router as router_shop
from app.user.router import router as router_user
from fastapi import FastAPI, Request

app = FastAPI(
    title="HomeWork_1_app",
    description=("hw_app"),
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)

app.include_router(router_shop)
app.include_router(router_user)
app.include_router(main_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware function that adds a custom header to the HTTP 
    response containing the time taken to process the request.

    Args:
        request (Request): The HTTP request object.
        call_next: The function to call to proceed with the request handling.

    Returns:
        Response: The modified HTTP response object with an additional
        custom header named "X-Process-Time" that contains the time
        taken to process the request.
    """
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
