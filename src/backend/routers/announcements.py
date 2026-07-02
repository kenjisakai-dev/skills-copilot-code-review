"""
Endpoints for managing announcements in the High School Management System API
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional, List
from datetime import datetime
from bson.objectid import ObjectId

from ..database import announcements_collection, teachers_collection

router = APIRouter(
    prefix="/announcements",
    tags=["announcements"]
)


@router.get("", response_model=List[Dict[str, Any]])
@router.get("/", response_model=List[Dict[str, Any]])
def get_announcements() -> List[Dict[str, Any]]:
    """Get all active announcements (not expired)"""
    now = datetime.now().strftime("%Y-%m-%d")
    
    # Query announcements that are either:
    # - Have no start_date, or start_date <= today
    # - Have expiration_date >= today
    query = {
        "$and": [
            {
                "$or": [
                    {"start_date": None},
                    {"start_date": {"$lte": now}}
                ]
            },
            {"expiration_date": {"$gte": now}}
        ]
    }
    
    announcements = []
    for announcement in announcements_collection.find(query).sort("created_at", -1):
        announcement["_id"] = str(announcement["_id"])
        announcements.append(announcement)
    
    return announcements


@router.get("/all", response_model=List[Dict[str, Any]])
def get_all_announcements() -> List[Dict[str, Any]]:
    """Get all announcements including expired ones (admin only)"""
    announcements = []
    for announcement in announcements_collection.find().sort("created_at", -1):
        announcement["_id"] = str(announcement["_id"])
        announcements.append(announcement)
    
    return announcements


@router.post("", response_model=Dict[str, Any])
def create_announcement(
    title: str,
    message: str,
    expiration_date: str,
    start_date: Optional[str] = None,
    teacher_username: Optional[str] = Query(None)
) -> Dict[str, Any]:
    """Create a new announcement (authenticated users only)"""
    # Check teacher authentication
    if not teacher_username:
        raise HTTPException(
            status_code=401, detail="Authentication required for this action"
        )
    
    teacher = teachers_collection.find_one({"_id": teacher_username})
    if not teacher:
        raise HTTPException(
            status_code=401, detail="Invalid teacher credentials"
        )
    
    # Validate dates
    try:
        exp_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        if start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            if start > exp_date:
                raise ValueError("Start date cannot be after expiration date")
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid date format or logic: {str(e)}"
        )
    
    # Create announcement
    announcement = {
        "_id": ObjectId(),
        "title": title,
        "message": message,
        "start_date": start_date,
        "expiration_date": expiration_date,
        "created_by": teacher_username,
        "created_at": datetime.now()
    }
    
    result = announcements_collection.insert_one(announcement)
    
    announcement["_id"] = str(announcement["_id"])
    return announcement


@router.put("/{announcement_id}", response_model=Dict[str, Any])
def update_announcement(
    announcement_id: str,
    title: Optional[str] = None,
    message: Optional[str] = None,
    expiration_date: Optional[str] = None,
    start_date: Optional[str] = None,
    teacher_username: Optional[str] = Query(None)
) -> Dict[str, Any]:
    """Update an announcement (authenticated users only)"""
    # Check teacher authentication
    if not teacher_username:
        raise HTTPException(
            status_code=401, detail="Authentication required for this action"
        )
    
    teacher = teachers_collection.find_one({"_id": teacher_username})
    if not teacher:
        raise HTTPException(
            status_code=401, detail="Invalid teacher credentials"
        )
    
    # Find announcement
    try:
        obj_id = ObjectId(announcement_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid announcement ID")
    
    announcement = announcements_collection.find_one({"_id": obj_id})
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    # Prepare update data
    update_data = {}
    
    if title is not None:
        update_data["title"] = title
    
    if message is not None:
        update_data["message"] = message
    
    if expiration_date is not None:
        try:
            datetime.strptime(expiration_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid expiration date format")
        update_data["expiration_date"] = expiration_date
    
    if start_date is not None:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start date format")
        update_data["start_date"] = start_date
    
    # Validate date logic
    final_exp_date = update_data.get("expiration_date", announcement.get("expiration_date"))
    final_start_date = update_data.get("start_date", announcement.get("start_date"))
    
    if final_start_date and final_exp_date:
        start = datetime.strptime(final_start_date, "%Y-%m-%d")
        exp = datetime.strptime(final_exp_date, "%Y-%m-%d")
        if start > exp:
            raise HTTPException(
                status_code=400, detail="Start date cannot be after expiration date"
            )
    
    # Update announcement
    result = announcements_collection.update_one(
        {"_id": obj_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update announcement")
    
    # Return updated announcement
    updated = announcements_collection.find_one({"_id": obj_id})
    updated["_id"] = str(updated["_id"])
    return updated


@router.delete("/{announcement_id}")
def delete_announcement(
    announcement_id: str,
    teacher_username: Optional[str] = Query(None)
) -> Dict[str, str]:
    """Delete an announcement (authenticated users only)"""
    # Check teacher authentication
    if not teacher_username:
        raise HTTPException(
            status_code=401, detail="Authentication required for this action"
        )
    
    teacher = teachers_collection.find_one({"_id": teacher_username})
    if not teacher:
        raise HTTPException(
            status_code=401, detail="Invalid teacher credentials"
        )
    
    # Find and delete announcement
    try:
        obj_id = ObjectId(announcement_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid announcement ID")
    
    result = announcements_collection.delete_one({"_id": obj_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    return {"message": "Announcement deleted successfully"}
