from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Config

async_engine = AsyncEngine(create_engine(
    url=Config.DATABASE_URL,
    echo=True
))


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:

    async_session_factory = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session_factory() as session:
        yield session