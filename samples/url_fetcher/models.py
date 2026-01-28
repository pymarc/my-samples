
from pydantic import BaseModel


class UrlFetchedData(BaseModel):
    """It's a model of unified data returned from URL fetching."""
    url: str
    status_code: int
    response_time: float
    content_type: str
    content_length: int
