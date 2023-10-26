from fastapi import FastAPI
import uvicorn

from app.router import router


app = FastAPI(
    title="HomeWork_3_app_main_api",
    description=("hw3 app (microservices)"),
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
