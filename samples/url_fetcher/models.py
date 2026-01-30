
from typing import Optional
from pydantic import BaseModel


class UrlFetchedData(BaseModel):
    """It's a model of unified data returned from URL fetching."""
    url: str
    status_code: Optional[int] = None
    response_time: float
    content_type: str = "unknown"
    content_length: int = 0
    error: Optional[str] = None
