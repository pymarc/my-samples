"""Project models."""
import json
import base64
import datetime
from pydantic import BaseModel, Field, field_validator


class EventCursor(BaseModel):
    """SQL cursor model."""
    occurred_at: datetime.datetime
    event_id: int = Field(gt=0)

    @classmethod
    def generate_from_base64(cls, base64_data: str) -> 'EventCursor':
        cursor_json_text = base64.b64decode(base64_data.encode('utf-8')).decode('utf-8')
        cursor_dict = json.loads(cursor_json_text)
        return cls(**cursor_dict)

    @field_validator("occurred_at")
    @classmethod
    def ensure_timezone(cls, v: datetime.datetime) -> datetime.datetime:
        if v.tzinfo is None:
            raise ValueError("occurred_at must be timezone-aware")
        return v

    @staticmethod
    def convert_postgres_timestamptz_to_datetime(datetime_text: str) -> datetime.datetime:
        datetime_text = datetime_text.replace(" ", "T", 1)
        if datetime_text.endswith("Z"):
            datetime_text = datetime_text[:-1] + "+00:00"
        return datetime.datetime.fromisoformat(datetime_text)

    @staticmethod
    def convert_datetime_to_postgres_timestamptz(datetime_tz: datetime.datetime) -> str:
        if datetime_tz.tzinfo is None:
            raise ValueError("datetime must be timezone-aware")
        datetime_text_isoformat = datetime_tz.isoformat()
        datetime_tz_text = datetime_text_isoformat.replace("T", " ", 1)
        if datetime_tz_text.endswith("+00:00"):
            datetime_tz_text = datetime_tz_text[:-6] + "Z"
        return datetime_tz_text
