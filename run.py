
import time

from samples.utils.timing import time_it


def x():
    time.sleep(3)
    return 1


if __name__ == '__main__':
    print("Starting the script...")
    with time_it(label='Function X'):
        x()
    print("Script finished.")