from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from query_db import add_items_db, delete_items_db, get_items_db, update_items_db
from schema import AddItems, GetItems, PutItems, PatchItems
from custom_exceptions import invalid_id

from redis_conf import check_cache_memory


router = APIRouter(prefix="/items", tags=["CRUD items"])


async def clear_cache_on_update(cache_id: int | None = None):
    await FastAPICache.clear(namespace="all_items")
    if cache_id:
        await FastAPICache.clear(namespace=f"item-{cache_id}")


@router.get("/{item_id}")
async def get_items(item_id: int) -> List[GetItems]:
    """
    Returns the item by the specified id from database.
    :param item_id:
    :return: List[GetItem]
    """
    if type(item_id) != int or item_id < 1:
        invalid_id()

    @cache(60, namespace=f"item-{item_id}")
    async def send_request_to_db():
        return await get_items_db(item_id_db=item_id)

    await check_cache_memory()
    return await send_request_to_db()


@router.post("")
async def new_items(item: AddItems = Depends()) -> str:
    """
    Adds a new item to the database.
    :param item:
    :return: str
    """
    await clear_cache_on_update()
    await add_items_db(item)
    return "done"


@router.put("/{item_id}")
async def update_items(item_id: int, data: PutItems = Depends()):
    """
    Updates all information about the product with the specified id.
    :param item_id:
    :param data:
    :return:
    """
    if type(item_id) != int or item_id < 1:
        invalid_id()

    await clear_cache_on_update(item_id)
    await update_items_db(item_id, data.dict())
    return "done"


@router.patch("/{item_id}")
async def partial_update_items(item_id: int, data: PatchItems = Depends()) -> str:
    """
    Updates partial information about the product with the specified id.
    :param item_id:
    :param data:
    :return:
    """
    if type(item_id) != int or item_id < 1:
        invalid_id()

    await clear_cache_on_update(item_id)
    await update_items_db(item_id, data.dict(exclude_none=True))
    return "done"


@router.delete("/{item_id}")
async def delete_items(item_id: int) -> str:
    """
    Deletes item with the passed id.
    :param item_id:
    :return: str
    """
    if type(item_id) != int or item_id < 1:
        invalid_id()

    await clear_cache_on_update(item_id)
    await delete_items_db(item_id)
    return "done"
