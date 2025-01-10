from typing import List, Optional
from app.models.items import ItemCreate, ItemUpdate, Item
import random  # Simulating database with a simple in-memory store

# In-memory "database"
fake_db = []


# Create a new item
def create_item(item: ItemCreate) -> Item:
    new_item = Item(id=len(fake_db) + 1, **item.dict())
    fake_db.append(new_item)
    return new_item


# Get all items
def get_items(skip: int = 0, limit: int = 10) -> List[Item]:
    return fake_db[skip: skip + limit]


# Get a single item by ID
def get_item(item_id: int) -> Optional[Item]:
    for item in fake_db:
        if item.id == item_id:
            return item
    return None


# Update an item by ID
def update_item(item_id: int, item_update: ItemUpdate) -> Optional[Item]:
    item = get_item(item_id)
    if item:
        updated_data = item.dict(exclude_unset=True)
        updated_data.update(item_update.dict(exclude_unset=True))
        updated_item = Item(**updated_data)

        # Replace the old item with the updated one
        fake_db[item.id - 1] = updated_item
        return updated_item
    return None


# Delete an item by ID
def delete_item(item_id: int) -> Optional[Item]:
    item = get_item(item_id)
    if item:
        fake_db.remove(item)
        return item
    return None
