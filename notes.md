# Advanced Typing in Python

## Protocol
It's like ABC but newer, it's more flexible.

Example:

```python
from typing import Protocol

class MyLogger(Protocol):
    def log(self, message: str) -> None:
        ...

class RealLogger:
    def log(self, message: str) -> None:
        print(message)

def use_logger(logger: MyLogger) -> None:
    logger.log("Hello, Protocol!")

real_logger = RealLogger()
use_logger(real_logger)
```
`mypy` will be happy because `RealLogger` has the required method.

PS. To run `mypy` execute `mypy your_file.py` or `mypy /my/dir`.

## Literal
It allows to define a set of strict values for a variable.

Example:

```python
from typing import Literal

def review_service(rating: Literal[1, 2, 3, 4, 5]) -> str:
    return f"Thank you for your {rating}-star review!"

# Not valid
review_service(10)  # mypy will complain
# Valid
review_service(5)
```

## TypedDict
It's for typing dictionaries.

Example:

```python
from typing import TypedDict, Literal

class EventDict(TypedDict):
    type: Literal["INFO", "ERROR"]
    msg: str
    ts: float

# This is valid
my_dict: EventDict = {
    "type": "INFO",
    "msg": "This is an info message.",
    "ts": 1625247600.0
}
```

## dataclass vs pydantic v2

### dataclass
Built-in, simple to use, no validation.

Example:

```python
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str

user = User(id=1, name="Alice")
print(user)
# Output: User(id=1, name='Alice')
```

### pydantic v2
More powerful, built-in validation, serialization.

Example:

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name: str

try:
    user =  User(id='not-an-int', name="Alice")
except ValidationError as e:
    print(e)
# Output: 1 validation error for User

try:
    user = User(id=1, name="Alice")
    print(user)
except ValidationError as e:
    print(e)
# Output: id=1 name='Alice'

# Serialization
user_dict = user.model_dump()
print(user_dict)
# Output: {'id': 1, 'name': 'Alice'}
```


## Function tools

* context manager = `__enter__` / `__exit__` or `@contextmanager` (setup/teardown in one place)
* generator (`yield`) = lazy sequence, saves memory
* `yield from` = delegation to another generator
* `batched(iterable, size)` → useful for processing data in chunks (do it yourself)
* `itertools.groupby` → aggregation by key on sorted data
* `functools.lru_cache` → memoization of expensive function calls
* `functools.partial` → preconfigured functions (e.g., `logger.info`)

