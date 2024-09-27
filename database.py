from datetime import datetime

from sqlalchemy import text, inspect
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

async_eng = create_async_engine(
    'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres', echo=False)

session = async_sessionmaker(async_eng, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class ShopDB(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    category: Mapped[str]
    manufacturer: Mapped[str]
    item_code: Mapped[int] = mapped_column(index=True, unique=True)
    description: Mapped[str]
    price: Mapped[int]
    quantity: Mapped[int]
    published: Mapped[bool] = mapped_column(default=True)
    time_create: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


async def create_table():
    """
    Create all tables.
    """
    async with async_eng.connect() as conn:
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
    if not (ShopDB.__tablename__ in tables):
        async with async_eng.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("table was created")
