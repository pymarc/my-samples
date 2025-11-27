Protocol → interfejs po metodach, nie po dziedziczeniu
TypedDict → typowane JSON-y
Literal → enumeracja bez Enum
dataclass → struktura bez walidacji
pydantic v2 → walidacja + serializacja (serde)

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
