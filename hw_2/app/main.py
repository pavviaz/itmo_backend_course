from fastapi import FastAPI

from app.auth.router import router as router_auth
from app.database import Base, engine
from app.auth.models import User


app = FastAPI(
    title="HomeWork_2_app",
    description=("hw2 app (todo-list with auth) with unit and integration tests"),
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
