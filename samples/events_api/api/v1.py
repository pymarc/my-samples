
from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/events")
async def get_events(limit: int = Query(10, ge=1, le=200)):
    """Get events with pagination/cursor."""
    return {"limit": limit, "items": [
        {"test": 1}
    ]}
