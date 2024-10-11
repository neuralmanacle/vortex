# routers/clock_in.py

from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from models.clock_in import ClockIn, ClockInCreate, ClockInUpdate
from database import clock_in_collection
from bson import ObjectId
from datetime import datetime
from pydantic import EmailStr

router = APIRouter(
    prefix="/clock-in",
    tags=["Clock-In Records"]
)

# Helper function to convert MongoDB document to ClockIn model
def clock_in_helper(record) -> ClockIn:
    return ClockIn(
        id=str(record["_id"]),
        email=record["email"],
        location=record["location"],
        insert_datetime=record["insert_datetime"]
    )

@router.post("/", response_model=ClockIn, status_code=status.HTTP_201_CREATED)
def create_clock_in(record: ClockInCreate):
    record_dict = record.dict()
    record_dict["insert_datetime"] = datetime.utcnow()
    result = clock_in_collection.insert_one(record_dict)
    created_record = clock_in_collection.find_one({"_id": result.inserted_id})
    return clock_in_helper(created_record)

@router.get("/{id}", response_model=ClockIn)
def get_clock_in(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    record = clock_in_collection.find_one({"_id": ObjectId(id)})
    if record:
        return clock_in_helper(record)
    else:
        raise HTTPException(status_code=404, detail="Clock-In record not found")

@router.get("/filter", response_model=List[ClockIn])
def filter_clock_ins(
    email: Optional[EmailStr] = Query(None, description="Exact match for email"),
    location: Optional[str] = Query(None, description="Exact match for location"),
    insert_datetime: Optional[datetime] = Query(None, description="Clock-ins after this datetime (ISO format)")
):
    query = {}
    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if insert_datetime:
        query["insert_datetime"] = {"$gt": insert_datetime}
    
    records = clock_in_collection.find(query)
    return [clock_in_helper(record) for record in records]

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clock_in(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = clock_in_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return
    else:
        raise HTTPException(status_code=404, detail="Clock-In record not found")

@router.put("/{id}", response_model=ClockIn)
def update_clock_in(id: str, record: ClockInUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    update_data = {k: v for k, v in record.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    result = clock_in_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )
    if result.matched_count == 1:
        updated_record = clock_in_collection.find_one({"_id": ObjectId(id)})
        return clock_in_helper(updated_record)
    else:
        raise HTTPException(status_code=404, detail="Clock-In record not found")
