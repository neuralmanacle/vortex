# routers/items.py

from fastapi import APIRouter, HTTPException, status, Query
from datetime import date, datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from models.items import Item, ItemCreate, ItemUpdate
from database import item_collection  # Ensure this is correct
from bson import ObjectId

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

# Helper function to convert MongoDB document to Item model
def item_helper(item) -> Item:
    return Item(
        id=str(item["_id"]),
        name=item["name"],
        email=item["email"],
        quantity=item["quantity"],
        expiry_date=item["expiry_date"].date() if item.get("expiry_date") else None,  # Convert to date
        insert_date=item["insert_date"].date() if item.get("insert_date") else None  # Convert to date
    )

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    try:
        item_dict = item.dict()
        
        # Convert insert_date to datetime
        item_dict["insert_date"] = datetime.utcnow()
        
        # Convert expiry_date to datetime if it's a date object
        if isinstance(item_dict.get("expiry_date"), date):
            item_dict["expiry_date"] = datetime.combine(item_dict["expiry_date"], datetime.min.time())
        
        result = item_collection.insert_one(item_dict)
        created_item = item_collection.find_one({"_id": result.inserted_id})
        return item_helper(created_item)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/{id}", response_model=Item)
def get_item(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    item = item_collection.find_one({"_id": ObjectId(id)})
    if item:
        return item_helper(item)
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@router.get("/filter", response_model=List[Item])
def filter_items(
    id: Optional[str] = Query(None, description="Exact match for Item ID"),
    email: Optional[EmailStr] = Query(None, description="Exact match for email"),
    expiry_date: Optional[date] = Query(None, description="Items expiring after this date (YYYY-MM-DD)"),
    insert_date: Optional[date] = Query(None, description="Items inserted after this date (YYYY-MM-DD)"),
    quantity: Optional[int] = Query(None, ge=0, description="Quantity greater than or equal to this number")
):
    query = {}
    
    # Validate and add ID filter
    if id:
        if ObjectId.is_valid(id):
            query["_id"] = ObjectId(id)
        else:
            raise HTTPException(status_code=400, detail="Invalid ID format")

    # Add other filters to the query if they are provided
    if email:
        query["email"] = email
    if expiry_date:
        query["expiry_date"] = {"$gt": datetime.combine(expiry_date, datetime.min.time())}
    if insert_date:
        query["insert_date"] = {"$gt": datetime.combine(insert_date, datetime.min.time())}
    if quantity is not None:
        query["quantity"] = {"$gte": quantity}
    
    try:
        items = item_collection.find(query)
        return [item_helper(item) for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
@router.get("/aggregate/count-by-email", response_model=List[dict])
def count_items_by_email():
    pipeline = [
        {"$group": {"_id": "$email", "count": {"$sum": 1}}}
    ]
    aggregation = item_collection.aggregate(pipeline)
    return [{"email": doc["_id"], "count": doc["count"]} for doc in aggregation]

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = item_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@router.put("/{id}", response_model=Item)
def update_item(id: str, item: ItemUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    update_data = {k: v for k, v in item.dict().items() if v is not None}
    
    if "expiry_date" in update_data and isinstance(update_data["expiry_date"], date):
        update_data["expiry_date"] = datetime.combine(update_data["expiry_date"], datetime.min.time())
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    
    result = item_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 1:
        updated_item = item_collection.find_one({"_id": ObjectId(id)})
        return item_helper(updated_item)
    else:
        raise HTTPException(status_code=404, detail="Item not found")
