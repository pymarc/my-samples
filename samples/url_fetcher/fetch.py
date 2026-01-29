"""It's a module for fetching basic information about an address.

Example:
    >> python fetch.py --urls https://8.8.8.8 https://onet.pl https://mbank.pl --concurrency 5
"""

import time
import asyncio
from argparse import ArgumentParser
from asyncio import Semaphore
from httpx import AsyncClient

from samples.url_fetcher.models import UrlFetchedData
from samples.utils.timing import time_it


async def fetch_url_data(url: str, semaphore: Semaphore) -> UrlFetchedData:
    async with semaphore, AsyncClient() as client:
        t0 = time.perf_counter()
        response = await client.get(url, timeout=6, follow_redirects=True)
        response_time: float = round(time.perf_counter() - t0, 3)
        return UrlFetchedData(
            url=url,
            status_code=response.status_code,
            response_time=response_time,
            content_type=response.headers.get('Content-Type', 'unknown'),
            content_length=len(response.content)
        )


async def run(urls: list[str], semaphore: Semaphore) -> None:
    results: tuple[UrlFetchedData] = await asyncio.gather(
        *[fetch_url_data(url_, semaphore) for url_ in urls],
        return_exceptions=True
    )
    print(results)


if __name__ == '__main__':
    parser = ArgumentParser(description="A simple URL fetcher.")
    parser.add_argument('-u', '--urls', nargs='+', type=str, required=True, help='List of URLs to fetch')
    parser.add_argument('-c', '--concurrency', type=int, default=5, help='Number of concurrent requests')
    args = parser.parse_args()
    # Set limitation for concurrent tasks
    semaphore_ = Semaphore(args.concurrency)
    # Process URLs
    print(f"Start processing {len(args.urls)} URLs...")
    with time_it(label="Duration of the whole process"):
        asyncio.run(run(args.urls, semaphore_))
    print("The URLs are processed!")
