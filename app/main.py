from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import admin, events, health
from app.core.config import get_settings
from app.db.database import Base, engine

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)


@app.get("/version")
def get_version():
    return settings.version_payload()


app.include_router(health.router)
app.include_router(events.router)
app.include_router(admin.router)
