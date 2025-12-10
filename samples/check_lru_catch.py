"""This is the script output:

CacheInfo(hits=0, misses=0, maxsize=3, currsize=0)
[n=2] Execution time: 2.000421 seconds
CacheInfo(hits=0, misses=1, maxsize=3, currsize=1)
[n=2] Execution time: 0.000002 seconds
CacheInfo(hits=1, misses=1, maxsize=3, currsize=1)
[n=2] Execution time: 0.000001 seconds
CacheInfo(hits=2, misses=1, maxsize=3, currsize=1)
[n=4] Execution time: 4.001144 seconds
CacheInfo(hits=2, misses=2, maxsize=3, currsize=2)
[n=4] Execution time: 0.000002 seconds
CacheInfo(hits=3, misses=2, maxsize=3, currsize=2)
[n=5] Execution time: 5.000159 seconds
CacheInfo(hits=3, misses=3, maxsize=3, currsize=3)
[n=5] Execution time: 0.000003 seconds
CacheInfo(hits=4, misses=3, maxsize=3, currsize=3)
[n=6] Execution time: 6.000871 seconds
CacheInfo(hits=4, misses=4, maxsize=3, currsize=3)
[n=6] Execution time: 0.000002 seconds
CacheInfo(hits=5, misses=4, maxsize=3, currsize=3)
[n=2] Execution time: 2.000888 seconds
CacheInfo(hits=5, misses=5, maxsize=3, currsize=3)
[n=2] Execution time: 0.000002 seconds
CacheInfo(hits=6, misses=5, maxsize=3, currsize=3)

Fields explained:
1. hits — number of times a call returned a cached result (cache hits).
2. misses — number of times the function had to compute and store a result (cache misses).
3. maxsize — configured maximum number of cached entries. `None` means unbounded.
4. currsize — current number of entries stored in the cache.
"""
import time
from functools import lru_cache

from samples.utils.timing import time_it


@lru_cache(maxsize=3)
def long_running_task(n: int):
    time.sleep(n)
    return 1


if __name__ == '__main__':
    print(long_running_task.cache_info())

    with time_it(label="n=2"):
        long_running_task(2)
    print(long_running_task.cache_info())
    with time_it(label="n=2"):
        long_running_task(2)
    print(long_running_task.cache_info())
    with time_it(label="n=2"):
        long_running_task(2)
    print(long_running_task.cache_info())

    with time_it(label="n=4"):
        long_running_task(4)
    print(long_running_task.cache_info())
    with time_it(label="n=4"):
        long_running_task(4)
    print(long_running_task.cache_info())

    with time_it(label="n=5"):
        long_running_task(5)
    print(long_running_task.cache_info())
    with time_it(label="n=5"):
        long_running_task(5)
    print(long_running_task.cache_info())

    with time_it(label="n=6"):
        long_running_task(6)
    print(long_running_task.cache_info())
    with time_it(label="n=6"):
        long_running_task(6)
    print(long_running_task.cache_info())

    with time_it(label="n=2"):
        long_running_task(2)
    print(long_running_task.cache_info())
    with time_it(label="n=2"):
        long_running_task(2)
    print(long_running_task.cache_info())

