
import pytest
import httpx
from asyncio import Semaphore

from samples.url_fetcher.fetch import fetch_url_data
from samples.url_fetcher.models import UrlFetchedData


def test_url_fetched_data_model():
    data = UrlFetchedData(
        url="https://example.com",
        status_code=200,
        response_time=0.123,
        content_type="text/html",
        content_length=100,
    )

    assert data.url == "https://example.com"
    assert data.status_code == 200
    assert isinstance(data.response_time, float)
    assert data.content_type == "text/html"
    assert data.content_length == 100
    assert data.error is None


def test_url_fetched_data_model_with_error():
    address = "https://fake-address-wdu8328q.xd"
    expected_error = "[Errno -2] Name or service not known"
    data = UrlFetchedData(
        url=address,
        response_time=0.456,
        error=expected_error
    )

    assert data.url == address
    assert data.status_code is None
    assert isinstance(data.response_time, float)
    assert data.content_type == "unknown"
    assert data.content_length == 0
    assert data.error == expected_error


@pytest.mark.asyncio
async def test_fetch_url_data_success():
    url = "https://example.com"
    expected_response_content = b"Plain text: 132234"

    async def handler(request):
        return httpx.Response(
            200,
            content=expected_response_content, headers={"Content-Type": "text/plain"}
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        semaphore = Semaphore(2)
        result = await fetch_url_data(url, semaphore, client)
        assert isinstance(result, UrlFetchedData)
        assert result.url == url
        assert result.status_code == 200
        assert isinstance(result.response_time, float)
        assert result.response_time >= 0.0
        assert result.content_type == "text/plain"
        assert result.content_length == len(expected_response_content)
        assert result.error is None
