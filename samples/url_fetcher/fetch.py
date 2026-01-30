"""It's a module for fetching basic information about an address.

Example:
    >> python fetch.py --urls https://8.8.8.8 https://onet.pl https://mbank.pl --concurrency 5
"""

import time
import asyncio
from argparse import ArgumentParser
from asyncio import Semaphore
from httpx import AsyncClient, Timeout, HTTPError

from samples.url_fetcher.models import UrlFetchedData
from samples.utils.timing import time_it


async def fetch_url_data(url: str, semaphore: Semaphore, client: AsyncClient) -> UrlFetchedData:
    async with semaphore:
        t0 = time.perf_counter()
        try:
            response = await client.get(url, follow_redirects=True)
            response_time: float = round(time.perf_counter() - t0, 3)
            return UrlFetchedData(
                url=url,
                status_code=response.status_code,
                response_time=response_time,
                content_type=response.headers.get('Content-Type', 'unknown'),
                content_length=len(response.content)
            )
        except HTTPError as e:
            response_time = round(time.perf_counter() - t0, 3)
            return UrlFetchedData(
                url=url,
                response_time=response_time,
                error=str(e)
            )


async def run(urls: list[str], semaphore: Semaphore, output_jsonl_file=None) -> None:
    timeout = Timeout(6.0)
    # Use just one client for all requests to take advantage of connection pooling
    # and increase performance.
    async with AsyncClient(timeout=timeout) as client:
        results: tuple[UrlFetchedData] = await asyncio.gather(
            *(fetch_url_data(url_, semaphore, client) for url_ in urls)
        )
    print(results)
    if output_jsonl_file is not None:
        with open(output_jsonl_file, 'w', encoding='utf-8') as f:
            for result in results:
                f.write(result.model_dump_json(exclude_none=True, ensure_ascii=False) + '\n')
            print("Results are saved to", output_jsonl_file)


def main():
    parser = ArgumentParser(description="A simple URL fetcher.")
    parser.add_argument('-u', '--urls', nargs='+', type=str, required=True, help='List of URLs to fetch')
    parser.add_argument('-c', '--concurrency', type=int, default=5, help='Number of concurrent requests')
    parser.add_argument('-o', '--output-jsonl-file', type=str, default=None, help='Output JSONL file path')
    args = parser.parse_args()
    # Set limitation for concurrent tasks
    semaphore_ = Semaphore(args.concurrency)
    # Process URLs
    print(f"Start processing {len(args.urls)} URLs...")
    with time_it(label="Duration of the whole process"):
        asyncio.run(run(args.urls, semaphore_))
    print("The URLs are processed!")


if __name__ == '__main__':
    main()
