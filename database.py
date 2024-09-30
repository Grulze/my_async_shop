from datetime import datetime
from logging import getLogger

from sqlalchemy import text, inspect, BigInteger, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

logger = getLogger(__name__)

async_eng = create_async_engine(
    'postgresql+asyncpg://postgres:postgres@db:5432/postgres', echo=False)

session = async_sessionmaker(async_eng, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class ShopDB(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(String(50), index=True)
    category = mapped_column(String(30))
    manufacturer = mapped_column(String(30))
    item_code = mapped_column(BigInteger, index=True, unique=True)
    description = mapped_column(String(400))
    price: Mapped[int]
    quantity: Mapped[int]
    published: Mapped[bool] = mapped_column(default=True)
    time_create: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


async def create_table():
    """
    Create all tables.
    """
    logger.info("Checking for tables")

    async with async_eng.connect() as conn:
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())

    logger.info("Checking the availability of the necessary tables")

    if not (ShopDB.__tablename__ in tables):
        async with async_eng.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Table was created")
