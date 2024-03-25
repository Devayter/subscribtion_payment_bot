from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)
from sqlalchemy.orm import (
    declarative_base, declared_attr, Mapped, mapped_column
)

from core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


Base = declarative_base(cls=PreBase)
engine = create_async_engine(settings.database_url)
async_session = async_sessionmaker(engine, class_=AsyncSession)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
