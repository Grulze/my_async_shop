from fastapi import HTTPException


def raise_exception(status: int = 400, info: str = "something went wrong"):
    raise HTTPException(status_code=status, detail=info)


def invalid_id(http_status: int = 400, message: str = "item_id must be a positive integer number"):
    raise_exception(status=http_status, info=message)


def non_existent_object(http_status: int = 404, message: str = "there are no objects with this item_id"):
    raise_exception(status=http_status, info=message)


def existing_item_code(http_status: int = 400, message: str = "This item code already exists, we need a unique one"):
    raise_exception(status=http_status, info=message)
