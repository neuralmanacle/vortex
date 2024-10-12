# routers/clock_in.py

from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from models.clock_in import ClockIn, ClockInCreate, ClockInUpdate
from database import clock_in_collection
from bson import ObjectId
from datetime import datetime, date
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
        insert_datetime=record["insert_datetime"].isoformat() if isinstance(record["insert_datetime"], date) else record["insert_datetime"]
    )

@router.post("/", response_model=ClockIn, status_code=status.HTTP_201_CREATED)
def create_clock_in(record: ClockInCreate):
    try:
        record_dict = record.dict()
        record_dict["insert_datetime"] = datetime.utcnow()  # Store complete datetime
        result = clock_in_collection.insert_one(record_dict)
        created_record = clock_in_collection.find_one({"_id": result.inserted_id})
        return clock_in_helper(created_record)
    except Exception as e:
        # Catch any internal server errors during record creation
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.get("/{id}", response_model=ClockIn)
def get_clock_in(id: str):
    logger.info(f"Received ID: {id}")  # Log the received ID
    if not ObjectId.is_valid(id):
        logger.error(f"Invalid ID format: {id}")  # Log the error
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    try:
        record = clock_in_collection.find_one({"_id": ObjectId(id)})
        if record:
            return clock_in_helper(record)
        else:
            logger.warning(f"Clock-In record not found for ID: {id}")  # Log if record is not found
            raise HTTPException(status_code=404, detail="Clock-In record not found")
    except Exception as e:
        logger.error(f"Internal server error: {str(e)}")  # Log internal server errors
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.get("/filter", response_model=List[ClockIn])
def filter_clock_ins(
    id: Optional[str] = Query(None, description="Exact match for Clock-In ID"),
    email: Optional[EmailStr] = Query(None, description="Exact match for email"),
    location: Optional[str] = Query(None, description="Exact match for location"),
    insert_datetime: Optional[date] = Query(None, description="Clock-ins after this date (YYYY-MM-DD)")
):
    query = {}
    
    # Add filters to the query if they are provided
    if id and ObjectId.is_valid(id):
        query["_id"] = ObjectId(id)  # Use ObjectId for filtering by ID
    elif id:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if insert_datetime:
        query["insert_datetime"] = {"$gt": insert_datetime}
    
    try:
        records = clock_in_collection.find(query)
        return [clock_in_helper(record) for record in records]
    except Exception as e:
        # Catching any internal server errors for the filtering
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clock_in(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    try:
        result = clock_in_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return
        else:
            raise HTTPException(status_code=404, detail="Clock-In record not found")
    except Exception as e:
        # Catch any internal server errors during deletion
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.put("/{id}", response_model=ClockIn)
def update_clock_in(id: str, record: ClockInUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    try:
        update_data = {k: v for k, v in record.dict().items() if v is not None}

        # If updating the insert_datetime, ensure it's in the correct format
        if "insert_datetime" in update_data:
            update_data["insert_datetime"] = update_data["insert_datetime"].date()  # Ensure it is a date

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
    except Exception as e:
        # Catch any internal server errors during update
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
