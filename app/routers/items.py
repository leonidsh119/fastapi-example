from fastapi import APIRouter, HTTPException
from app.models.items import Item, ItemCreate, ItemUpdate
from app.services.items import create_item, get_items, get_item, update_item, delete_item
from typing import List

router = APIRouter()

@router.post("/", response_model=Item)
async def create_item_endpoint(item: ItemCreate):
    created_item = create_item(item)
    return created_item

@router.get("/", response_model=List[Item])
async def get_items_endpoint(skip: int = 0, limit: int = 10):
    items = get_items(skip=skip, limit=limit)
    return items

@router.get("/{item_id}", response_model=Item)
async def get_item_endpoint(item_id: int):
    item = get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=Item)
async def update_item_endpoint(item_id: int, item_update: ItemUpdate):
    updated_item = update_item(item_id, item_update)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/{item_id}", response_model=Item)
async def delete_item_endpoint(item_id: int):
    deleted_item = delete_item(item_id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_item
