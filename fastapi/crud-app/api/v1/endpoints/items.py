from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from crud import crud_item
from models.item import Item
from schemas.item import ItemCreate, ItemUpdate, ItemInDB
from db.session import get_db
from core.logger import logger
from exceptions.http_exceptions import ItemNotFoundException, ItemAlreadyExistsException

router = APIRouter()

@router.get("/items/", response_model=List[ItemInDB], summary="Get all items")
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all items.

    - **skip**: Number of items to skip (pagination)
    - **limit**: Maximum number of items to return
    """
    items = crud_item.get_items(db, skip=skip, limit=limit)
    logger.info(f"Retrieved {len(items)} items")
    return items

@router.post("/items/", response_model=ItemInDB, summary="Create a new item")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item.

    - **name**: Required. The name of the item
    - **description**: Optional. A description of the item
    """
    db_item = crud_item.get_item_by_name(db, name=item.name)
    if db_item:
        logger.warning(f"Attempt to create duplicate item: {item.name}")
        raise ItemAlreadyExistsException(name=item.name)
    return crud_item.create_item(db=db, item=item)

@router.get("/items/{item_id}", response_model=ItemInDB, summary="Get a specific item")
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get a specific item by ID.

    - **item_id**: Required. The ID of the item to retrieve
    """
    db_item = crud_item.get_item(db, item_id=item_id)
    if db_item is None:
        logger.warning(f"Item not found: {item_id}")
        raise ItemNotFoundException(item_id=item_id)
    return db_item

@router.put("/items/{item_id}", response_model=ItemInDB, summary="Update an item")
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    """
    Update an existing item.

    - **item_id**: Required. The ID of the item to update
    - **name**: Optional. The new name of the item
    - **description**: Optional. The new description of the item
    """
    db_item = crud_item.get_item(db, item_id=item_id)
    if db_item is None:
        logger.warning(f"Attempt to update non-existent item: {item_id}")
        raise ItemNotFoundException(item_id=item_id)
    return crud_item.update_item(db=db, item_id=item_id, item=item)

@router.delete("/items/{item_id}", response_model=ItemInDB, summary="Delete an item")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing item.

    - **item_id**: Required. The ID of the item to delete
    """
    db_item = crud_item.get_item(db, item_id=item_id)
    if db_item is None:
        logger.warning(f"Attempt to delete non-existent item: {item_id}")
        raise ItemNotFoundException(item_id=item_id)
    return crud_item.delete_item(db=db, item_id=item_id)
