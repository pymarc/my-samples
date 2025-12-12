"""A simple example of how to use asyncio."""
import asyncio

from samples.utils.timing import time_it


async def fetch_url(url):
    print("Start fetching URL (5s delay): " + url)
    await asyncio.sleep(5)
    print(f"Ended request to URL: {url}")
    return f"{url} response: success"


async def main():
    print("Starting tasks...")
    task_1 = asyncio.create_task(fetch_url('http://some.com'))
    task_2 = asyncio.create_task(fetch_url('http://another.some.com'))
    print("Tasks created!")
    print("Waiting for the tasks to finish...")
    await task_1
    await task_2
    print(f"Task 1 result: {task_1.result()}")
    print(f"Task 2 result: {task_2.result()}")


if __name__ == '__main__':
    with time_it(label="Total execution time of the program"):
        asyncio.run(main())
        print("There are two tasks, both taking 5 second. Is not the asynchronous run it would take 10 seconds.")
