from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.db.main import init_db
from src.donations.routes import donations_router
from src.users.routes import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Server is starting..')
    await init_db()
    yield
    print('Server is shutting down..')


version = "v1"
app = FastAPI(
    title='Donation',
    description="REST API for donation web project",
    version=version,
    lifespan=lifespan,
)
app.include_router(users_router)
app.include_router(donations_router)
