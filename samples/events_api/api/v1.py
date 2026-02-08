
import re
import base64
import asyncpg
import logging
from typing import Optional
from fastapi import APIRouter, Query, Depends, HTTPException

from ..db.pool import get_pool

router = APIRouter()


def decode_cursor(encoded_cursor: str) -> str:
    return base64.b64decode(encoded_cursor.encode('utf-8')).decode('utf-8')


def validate_cursor(plain_text_cursor: str) -> None:
    pattern = r'^\("(?P<dt>\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]) (?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d\.\d{1,6}(?:Z|[+-](?:0\d|1\d|2[0-3])(?::?[0-5]\d)?)?)", (?P<n>[1-9]\d*)\)$'
    assert re.fullmatch(pattern, plain_text_cursor), f"The cursor value '{plain_text_cursor}' is not valid!"


def validate_limit(limit: int) -> None:
    assert isinstance(limit, int), f"The limit value '{limit}' is not an integer!"
    assert limit > 0, f"The limit value '{limit}' has to be greater than 0!"


@router.get("/events")
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
        sql_query = "SELECT * FROM user_event "
        if cursor:
            decoded_cursor: str = decode_cursor(cursor)
            validate_cursor(decoded_cursor)
            validate_limit(limit)
            sql_query += f"WHERE (occurred_at, id) < {decoded_cursor} "
        sql_query += f"ORDER BY occurred_at DESC, id DESC LIMIT {limit}"

        # SQL query here
        async with pool.acquire() as conn:
            rows = await conn.fetch(sql_query)
            print(rows)
            # TODO: Finish here

        return {"limit": limit, "items": [
            {"test": 1}
        ]}
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail=str(e))
