import datetime
import asyncpg
import logging
from typing import Optional
from fastapi import APIRouter, Query, Depends, HTTPException

from ..db.pool import get_pool
from ..models import EventCursor, EventsResponse, Event

router = APIRouter()


@router.get("/events", response_model=EventsResponse)
async def get_events(
        limit: int = Query(10, ge=1, le=200),
        cursor: Optional[str] = Query(default=None),
        pool: asyncpg.Pool = Depends(get_pool),
):
    """Get events with pagination/cursor.

    :param limit: Number of events to return
    :param cursor: Encoded cursor showing where to start getting events from DB.
        Decoded form is (occurred_at, id_of_event).
    :param pool: Connection pool.
    """
    try:
        sql_query = """
        SELECT id AS event_id, user_name, event_type, data, occurred_at
        FROM user_event
        WHERE
          ($1::timestamptz IS NULL OR (occurred_at, id) < ($1, $2))
        ORDER BY occurred_at DESC, id DESC
        LIMIT $3
        """
        occurred_at: Optional[datetime.datetime] = None
        event_id: Optional[int] = None
        if cursor:
            event_cursor = EventCursor.generate_from_base64(cursor)
            occurred_at = event_cursor.occurred_at
            event_id = event_cursor.event_id

        async with pool.acquire() as conn:
            rows = await conn.fetch(sql_query, occurred_at, event_id, limit)
            items: list[Event] = [Event(**dict(row)) for row in rows]

        next_cursor: Optional[str] = None
        if items:
            last_event: Event = items[-1]
            next_event_cursor = EventCursor(
                occurred_at=last_event.occurred_at,
                event_id=last_event.event_id
            )
            next_cursor = next_event_cursor.get_cursor_base64()

        return EventsResponse(
            limit=limit,
            items=items,
            next_cursor=next_cursor
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logging.exception("Unhandled error in GET /events")
        raise HTTPException(status_code=500, detail="Internal server error")
