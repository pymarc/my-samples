
import time
from contextlib import contextmanager


@contextmanager
def time_it(label=None):
    t0 = time.perf_counter()
    try:
        yield
    finally:
        dt = time.perf_counter() - t0
        label = f"[{label}] " if label else ""
        print(f"{label}Execution time: {dt:.6f} seconds")
