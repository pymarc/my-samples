"""A simple example of how to use asyncio."""
import asyncio

from samples.utils.timing import time_it


semaphore = asyncio.Semaphore(5)


async def fetch_url(url):
    print("Start fetching URL (5s delay): " + url)
    await asyncio.sleep(5)
    print(f"Ended request to URL: {url}")
    return f"{url} response: success"


async def semaphored_fetch_url(url):
    async with semaphore:
        return await fetch_url(url)


async def main_1():
    """Here we start every task separately and explicitly await them."""
    print("Starting tasks...")
    task_1 = asyncio.create_task(fetch_url('http://some.com'))
    task_2 = asyncio.create_task(fetch_url('http://another.some.com'))
    print("Tasks created!")
    print("Waiting for the tasks to finish...")
    await task_1
    await task_2
    print(f"Task 1 result: {task_1.result()}")
    print(f"Task 2 result: {task_2.result()}")


async def main_2():
    """Here we use `asyncio.gather` to create and await the tasks at one place.
    It still has a problem that it can overload a server.
    """
    print("Waiting for the tasks to finish...")
    results = await asyncio.gather(
        fetch_url('http://some.com'), fetch_url('http://another.some.com')
    )
    print(f"Task 1 and 2 results: {results}")


async def main_3():
    """It's a case where we are using Semaphore limitation to maximum 5 tasks at a time."""
    print("Waiting for the tasks to finish (Semaphore)...")
    results = await asyncio.gather(
        semaphored_fetch_url('http://some.com'), semaphored_fetch_url('http://another.some.com')
    )
    print(f"Task 1 and 2 results (Semaphore): {results}")


if __name__ == '__main__':
    with time_it(label="Total execution time of the program"):
        asyncio.run(main_3())
        print("There are two tasks, both taking 5 second. Is not the asynchronous run it would take 10 seconds.")
