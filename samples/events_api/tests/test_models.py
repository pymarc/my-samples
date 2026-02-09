"""Tests for models.py"""
import json
import base64
import datetime

from ..models import EventCursor


def test_generate_from_base64():
    expected_occurred_at = datetime.datetime(
        2026, 2, 9, 13, 00,
        tzinfo=datetime.timezone.utc
    )
    expected_event_id = 2345

    payload = {
        "occurred_at": expected_occurred_at.isoformat(),
        "event_id": 2345
    }
    cursor_base64 = base64.b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')

    event_cursor = EventCursor.generate_from_base64(cursor_base64)
    assert event_cursor.occurred_at == expected_occurred_at
    assert event_cursor.event_id == expected_event_id
