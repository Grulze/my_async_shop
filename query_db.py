from typing import List

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from database import ShopDB, session
from schema import AddItems, GetItems
from custom_exceptions import non_existent_object, existing_item_code


async def get_items_db(item_id_db: int | None = None, lim: int | None = None, page: int | None = None
                       ) -> List[GetItems]:
    async with session() as ses:
        if item_id_db:
            query = select(ShopDB).where(ShopDB.id == item_id_db)
        else:
            query = select(ShopDB).limit(lim).offset(page * lim)

        response = await ses.execute(query)
        task_set = response.scalars().all()

        if not task_set and item_id_db:
            non_existent_object()
        elif not task_set:
            non_existent_object(message="at this moment there are no objects in database")

        for task in task_set:
            task.time_create = task.time_create.replace(microsecond=0)

        return task_set


async def add_items_db(item: AddItems):
    async with session() as ses:
        item_data = item.model_dump()
        item_bd = ShopDB(**item_data)
        ses.add(item_bd)
        try:
            await ses.commit()
        except IntegrityError:
            existing_item_code()


async def update_items_db(item_id_db: int, values):
    async with session() as ses:
        await ses.execute(update(ShopDB).where(ShopDB.id == item_id_db).values(values))
        await ses.commit()


async def delete_items_db(item_id_db: int):
    async with session() as ses:
        await ses.execute(delete(ShopDB).where(ShopDB.id == item_id_db))
        await ses.commit()