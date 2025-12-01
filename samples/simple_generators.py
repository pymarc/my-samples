
def sub_generator():
    yield 3
    yield 4


def main_generator():
    yield 1
    yield 2
    yield from sub_generator()
    yield 5


def batched(iterable, size: int):
    start_index = 0
    end_index = size
    while True:
        batch = iterable[start_index:end_index]
        if not batch:
            break
        yield batch
        start_index = end_index
        end_index += size


if __name__ == '__main__':
    long_list = list(range(50))
    for v in batched(long_list, size=5):
        print(v)
