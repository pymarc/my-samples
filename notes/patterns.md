# Design Patterns – Quick Reference (Python)

## Creational Patterns

### Singleton
Ensures that a class has only one instance and provides a global access point to it.
Useful for shared resources like DB pools or configs.

```python
class DB:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
````

---

### Factory Method

Encapsulates object creation logic in one place, so the rest of the code doesn't depend on concrete classes.

```python
def create_client(kind):
    if kind == "a":
        return A()
    elif kind == "b":
        return B()
    raise ValueError("Unknown type")
```

---

### Builder

Constructs complex objects step by step, improving readability and avoiding large constructors with many parameters.

```python
class Builder:
    def __init__(self):
        self.data = {}

    def x(self, value):
        self.data["x"] = value
        return self

    def build(self):
        return self.data

obj = Builder().x(1).build()
```

---

## Structural Patterns

### Adapter

Converts one interface into another expected by the system, allowing incompatible classes to work together.

```python
class Adapter:
    def __init__(self, obj):
        self.obj = obj

    def run(self):
        return self.obj.execute()
```

---

### Decorator

Dynamically adds behavior to functions or objects without modifying their original code.

```python
def log(func):
    def wrapper(*args, **kwargs):
        print("start")
        return func(*args, **kwargs)
    return wrapper

@log
def f():
    pass
```

---

### Facade

Provides a simplified interface to a complex system, hiding internal details and reducing coupling.

```python
class Facade:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def run(self):
        x = self.a.step()
        return self.b.step(x)
```

---

## Behavioral Patterns

### Strategy

Defines a family of algorithms and makes them interchangeable at runtime without changing the client code.

```python
class Service:
    def __init__(self, strategy):
        self.strategy = strategy

    def run(self, x):
        return self.strategy(x)

def algo(x):
    return x * 2

Service(algo).run(3)
```

---

### Observer

Allows objects to subscribe to events and be notified when something happens, enabling loose coupling.

```python
subscribers = []

def subscribe(fn):
    subscribers.append(fn)

def notify(data):
    for fn in subscribers:
        fn(data)
```

---

### Command

Encapsulates a request as an object, allowing you to queue, log, retry, or execute it later.

```python
class Command:
    def __init__(self, value):
        self.value = value

    def execute(self):
        print(self.value)

cmd = Command("hello")
cmd.execute()
```

---

## Core Concepts (Very Important)

### Dependency Injection (DI)

Instead of creating dependencies inside a class, they are passed from outside, improving testability and flexibility.

```python
class Service:
    def __init__(self, repo):
        self.repo = repo
```

---

### Fluent API

A style of API design where methods return the object itself, enabling readable method chaining.

```python
obj = Builder().x(1).y(2).build()
```

---

## Abstract Factory

**Creates families of related objects without specifying their concrete classes.**

### Idea

Choose one "variant" (e.g. Postgres, MySQL) and get all compatible objects from it.

You can think of it like an IKEA kitchen set:

> You buy a set (countertop, cabinets, hinges) and everything fits together
> because it comes from one factory.


### Example

```python
class PostgresFactory:
    def create_repo(self):
        return PostgresRepo()

class MySQLFactory:
    def create_repo(self):
        return MySQLRepo()

def run(factory):
    repo = factory.create_repo()
```

---

## Prototype

**Creates new objects by copying an existing one.**

### Idea

Clone instead of building from scratch and in that copied object change selected attributes.

### Example

```python
import copy

obj1 = {"a": [1, 2]}
obj2 = copy.deepcopy(obj1)
obj2["a"].append(3)
```

---

## Bridge

**Separates abstraction from implementation.**

### Idea

Avoid class explosion by composing instead of inheriting.

### Example

```python
class Device:
    def on(self): pass

class TV(Device):
    def on(self): print("TV ON")

class Remote:
    def __init__(self, device):
        self.device = device  # Here is the bridge

    def power(self):
        self.device.on()
```

---

## Composite

**Treats single objects and groups uniformly (tree structure).**

### Idea

Same interface for leaf and container.

### Example

```python
class File:
    def size(self): return 10

class Folder:
    def __init__(self):
        self.items = []

    def size(self):
        return sum(i.size() for i in self.items)
```

---

## Flyweight

**Reduces memory usage by sharing common parts of objects.**

---

### Idea
Avoid creating many identical objects.  
Store shared (intrinsic) data once and reuse it.

---

### Key Concept

```text
Intrinsic  = shared (stored inside object)
Extrinsic  = external (passed from outside)
````

---

### Example

```python
class Character:
    def __init__(self, char):
        self.char = char  # intrinsic (shared)


class CharacterFactory:
    _pool = {}

    @classmethod
    def get(cls, char):
        if char not in cls._pool:
            cls._pool[char] = Character(char)
        return cls._pool[char]


c1 = CharacterFactory.get("A")
c2 = CharacterFactory.get("A")

print(c1 is c2)  # True
```

---

## Proxy

**Provides a wrapper that controls access to another object.**

---

### Idea
Add behavior (lazy loading, caching, security, logging)  
**without changing the original object.**

---

### Example (Lazy Loading)

```python
class RealService:
    def get_data(self):
        print("Loading data...")
        return [1, 2, 3]


class ProxyService:
    def __init__(self):
        self._real = None

    def get_data(self):
        if self._real is None:
            self._real = RealService()  # lazy initialization
        return self._real.get_data()


service = ProxyService()

service.get_data()  # creates RealService
service.get_data()  # reuses existing instance
````

---

### What’s happening

```text
Proxy → controls access
Real  → does the actual work
```

---

### Common use cases

* lazy loading
* caching results
* access control (auth)
* logging / monitoring
* remote calls (RPC, HTTP)

---

### Proxy types

* Lazy Proxy → creates object only when needed
* Cache Proxy → stores results
* Protection Proxy → checks permissions
* Logging Proxy → logs calls

---

### When to use

* you need control over access to an object
* object is expensive to create
* you want to add behavior transparently

---

### When NOT to use

* no extra logic needed
* simple direct access is enough

---

## Behavioral

## Iterator

**Provides a way to traverse a collection without exposing its internal structure.**

---

### Idea
Access elements sequentially without knowing how the collection is implemented.

---

### Example (Python built-in)

```python
for x in [1, 2, 3]:
    print(x)
````

The `for` loop uses an iterator internally.

---

### Manual iteration

```python
items = [1, 2, 3]

it = iter(items)

print(next(it))  # 1
print(next(it))  # 2
print(next(it))  # 3
```

---

### Custom iterator

```python
class Counter:
    def __init__(self, max):
        self.current = 0
        self.max = max

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.max:
            raise StopIteration
        self.current += 1
        return self.current


for x in Counter(3):
    print(x)
```

---

### Generator (Pythonic way)

```python
def counter(max):
    for i in range(1, max + 1):
        yield i


for x in counter(3):
    print(x)
```

---

### What’s happening

```text
Iterator → keeps state (position)
next()   → returns next element
StopIteration → signals end
```

---

### When to use

* large data (streaming)
* files
* paginated APIs
* lazy evaluation

---

### When NOT to use

* simple collections (Python handles it already)

---

### Quick summary

```text
Iterator = sequential access without exposing structure
```

---

## Template Method

**Defines the skeleton of an algorithm, allowing subclasses to override specific steps.**

---

### Idea
Keep the overall algorithm structure fixed, but allow certain steps to vary.

---

### Example

```python
class DataProcessor:
    def process(self):
        self.load()
        self.transform()
        self.save()

    def load(self): pass
    def transform(self): pass
    def save(self): pass


class CSVProcessor(DataProcessor):
    def load(self):
        print("Load CSV")

    def transform(self):
        print("Transform CSV")

    def save(self):
        print("Save CSV")


p = CSVProcessor()
p.process()
````

---

### What’s happening

```text
process() → defines the algorithm
steps     → can be overridden
```

---

### When to use

* fixed workflow (pipeline, ETL, request handling)
* steps vary, but order stays the same

---

### When NOT to use

* algorithm structure changes often
* you need full flexibility (use Strategy instead)

---

### Quick summary

```text
Template Method = fixed algorithm + customizable steps
```

---

## State

**Allows an object to change its behavior when its internal state changes.**

---

### Idea
Replace complex `if/else` logic with separate state objects.  
The context delegates behavior to the current state.

---

### Example

```python
class State:
    def handle(self, context):
        pass


class OffState(State):
    def handle(self, context):
        print("Turning ON")
        context.state = OnState()


class OnState(State):
    def handle(self, context):
        print("Turning OFF")
        context.state = OffState()


class Switch:
    def __init__(self):
        self.state = OffState()

    def press(self):
        self.state.handle(self)


s = Switch()
s.press()  # Turning ON
s.press()  # Turning OFF
````

---

### What’s happening

```text
Context → delegates to State
State   → can change Context state
```

---

### When to use

* state machines (FSM)
* workflows (order → paid → shipped)
* UI states (active, disabled)
* game logic (player states)

---

### When NOT to use

* very few simple states
* simple if/else is clearer

---

### Quick summary

```text
State = behavior depends on current state object
```

---

## Visitor

**Lets you add new operations to objects without modifying their classes.**

---

### Idea
Move operations out of object classes into separate visitor classes.

---

### Example

```python
class Visitor:
    def visit_user(self, user): pass
    def visit_order(self, order): pass


class PrintVisitor(Visitor):
    def visit_user(self, user):
        print("User:", user.name)

    def visit_order(self, order):
        print("Order:", order.id)


class User:
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        visitor.visit_user(self)


class Order:
    def __init__(self, id):
        self.id = id

    def accept(self, visitor):
        visitor.visit_order(self)


visitor = PrintVisitor()

User("Marcin").accept(visitor)
Order(123).accept(visitor)
````

---

### What’s happening

```text
element.accept(visitor) → calls visitor method
visitor → executes operation for that type
```

---

### When to use

* adding new operations frequently
* working with object structures (trees, AST)
* exporting, printing, validation

---

### When NOT to use

* object types change often (Visitor becomes hard to maintain)
* simple logic (overengineering)

---

### Quick summary

```text
Visitor = add new operations without modifying existing classes
```

---

## Mediator

**Centralizes communication between objects to reduce direct dependencies.**

---

### Idea
Objects don’t communicate directly with each other.  
They interact through a mediator (central hub).

---

### Example

```python
class ChatRoom:
    def send(self, message, user):
        print(f"{user.name}: {message}")


class User:
    def __init__(self, name, mediator):
        self.name = name
        self.mediator = mediator

    def send(self, message):
        self.mediator.send(message, self)


room = ChatRoom()

u1 = User("Marcin", room)
u2 = User("Patrycja", room)

u1.send("Hi!")
````

---

### What’s happening

```text
User → Mediator → handles communication
Users don’t talk to each other directly
```

---

### When to use

* many interacting objects (to avoid tight coupling)
* GUI components
* chat systems
* workflow coordination

---

### When NOT to use

* few objects
* simple direct communication is enough

---

### Quick summary

```text
Mediator = objects communicate through a central hub
```

---

### Memento
> Captures and restores an object's internal state (undo/rollback).

---

### Interpreter
> Defines a grammar and interprets sentences in that language (DSLs).

---

## Partially Covered / Mentioned

### Chain of Responsibility
> Passes a request along a chain of handlers until one handles it.
