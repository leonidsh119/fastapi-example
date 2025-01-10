from pydantic import BaseModel
from typing import Optional

# Pydantic model for the item (Create and Update)
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None

# Pydantic model for item creation
class ItemCreate(ItemBase):
    pass

# Pydantic model for item update (it can accept partial updates)
class ItemUpdate(ItemBase):
    pass

# Pydantic model for item response (including id)
class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True
