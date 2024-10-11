# models/items.py

from pydantic import BaseModel, Field, EmailStr
from datetime import date
from bson import ObjectId
# models/items.py

from pydantic import BaseModel, EmailStr, Field
from datetime import date
from bson import ObjectId

class ItemBase(BaseModel):
    name: str = Field(..., example="Apple")
    email: EmailStr
    quantity: int = Field(..., ge=0, example=10)
    expiry_date: date = Field(..., example="2024-12-31")

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: str = Field(None, example="Apple")
    email: EmailStr = None
    quantity: int = Field(None, ge=0, example=10)
    expiry_date: date = Field(None, example="2024-12-31")

class Item(ItemBase):
    id: str
    insert_date: date

    class Config:
        orm_mode = True

class ItemBase(BaseModel):
    name: str = Field(..., example="Apple")
    email: EmailStr
    quantity: int = Field(..., ge=0, example=10)
    expiry_date: date = Field(..., example="2024-12-31")

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: str = Field(None, example="Apple")
    email: EmailStr = None
    quantity: int = Field(None, ge=0, example=10)
    expiry_date: date = Field(None, example="2024-12-31")

class Item(ItemBase):
    id: str
    insert_date: date

    class Config:
        orm_mode = True
