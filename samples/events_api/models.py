import re
import base64
import datetime
from pydantic import BaseModel


class EventCursor(BaseModel):
    occurred_at: datetime.datetime
    event_id: int

    @classmethod
    def generate_from_base64(cls, base64_data: str) -> 'EventCursor':
        cursor_text = base64.b64decode(base64_data.encode('utf-8')).decode('utf-8')
        cls.validate_cursor_text(cursor_text)
        occurred_at_text, event_id_text = cursor_text.split(', ', 1)
        occurred_at: datetime.datetime = cls.convert_postgres_timestamptz_to_datetime(occurred_at_text)
        event_id = int(event_id_text)
        return cls(occurred_at=occurred_at, event_id=event_id)

    @staticmethod
    def validate_cursor_text(plain_text_cursor: str) -> None:
        pattern = r'^"(?P<dt>\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]) (?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d\.\d{1,6}(?:Z|[+-](?:0\d|1\d|2[0-3])(?::?[0-5]\d)?)?)", (?P<n>[1-9]\d*)$'
        assert re.fullmatch(pattern, plain_text_cursor), f"The cursor text value '{plain_text_cursor}' is not valid!"

    @staticmethod
    def convert_postgres_timestamptz_to_datetime(datetime_text: str) -> datetime.datetime:
        datetime_text = datetime_text.replace(" ", "T", 1)
        if datetime_text.endswith("Z"):
            datetime_text = datetime_text[:-1] + "+00:00"
        return datetime.datetime.fromisoformat(datetime_text)
