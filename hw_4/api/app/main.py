import os

import uvicorn
from fastapi import FastAPI

from app.downloader.router import router as router_dwnl
from app.root_router import router as root_router


app = FastAPI(
    title="Paper Downloader",
    description="Scientific paper downloader service",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)

app.include_router(router_dwnl)
app.include_router(root_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
