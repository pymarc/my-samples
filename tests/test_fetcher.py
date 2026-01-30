
import pytest
import httpx
import asyncio
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
    assert data.content_type == "unknown"
    assert data.content_length == 0
    assert data.error == expected_error