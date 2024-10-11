# models/clock_in.py

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from bson import ObjectId

class ClockInBase(BaseModel):
    email: EmailStr
    location: str = Field(..., example="New York")

class ClockInCreate(ClockInBase):
    pass

class ClockInUpdate(BaseModel):
    email: EmailStr = None
    location: str = Field(None, example="New York")

class ClockIn(ClockInBase):
    id: str
    insert_datetime: datetime

    class Config:
        orm_mode = True
