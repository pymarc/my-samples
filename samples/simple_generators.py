
def sub_generator():
    yield 3
    yield 4


def main_generator():
    yield 1
    yield 2
    yield from sub_generator()
    yield 5


if __name__ == '__main__':
    for v in main_generator():
        print(v)
