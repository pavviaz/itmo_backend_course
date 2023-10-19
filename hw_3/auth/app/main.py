from fastapi import FastAPI
import uvicorn

from app.aservice.router import router as router_auth
from app.database import Base, engine


app = FastAPI(
    title="HomeWork_3_app_auth_api",
    description=("hw3 auth api"),
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)

app.include_router(router_auth)


@app.on_event("startup")
async def init_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception:
        pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)