"""Project models."""
import json
import base64
import datetime
from pydantic import BaseModel, Field, field_validator


class EventCursor(BaseModel):
    """SQL cursor model."""
    occurred_at: datetime.datetime
    event_id: int = Field(gt=0)

    @field_validator("occurred_at")
    @classmethod
    def ensure_timezone(cls, v: datetime.datetime) -> datetime.datetime:
        if v.tzinfo is None:
            raise ValueError("occurred_at must be timezone-aware")
        return v

    @classmethod
    def generate_from_base64(cls, base64_data: str) -> 'EventCursor':
        cursor_json_text = base64.urlsafe_b64decode(base64_data.encode('utf-8')).decode('utf-8')
        cursor_dict = json.loads(cursor_json_text)
        return cls(**cursor_dict)

    def get_cursor_base64(self) -> str:
        occurred_at_str = self.occurred_at.isoformat()
        data = {
            "occurred_at": occurred_at_str,
            "event_id": self.event_id,
        }
        return base64.urlsafe_b64encode(json.dumps(data).encode('utf-8')).decode('utf-8')
