# Design Patterns – Quick Reference (Python)

## Creational Patterns

### Singleton
> Ensures that a class has only one instance and provides a global access point to it. Useful for shared resources like DB pools or configs.

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

> Encapsulates object creation logic in one place, so the rest of the code doesn’t depend on concrete classes.

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

> Constructs complex objects step by step, improving readability and avoiding large constructors with many parameters.

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

> Converts one interface into another expected by the system, allowing incompatible classes to work together.

```python
class Adapter:
    def __init__(self, obj):
        self.obj = obj

    def run(self):
        return self.obj.execute()
```

---

### Decorator

> Dynamically adds behavior to functions or objects without modifying their original code.

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

> Provides a simplified interface to a complex system, hiding internal details and reducing coupling.

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

> Defines a family of algorithms and makes them interchangeable at runtime without changing the client code.

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

> Allows objects to subscribe to events and be notified when something happens, enabling loose coupling.

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

> Encapsulates a request as an object, allowing you to queue, log, retry, or execute it later.

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

> Instead of creating dependencies inside a class, they are passed from outside, improving testability and flexibility.

```python
class Service:
    def __init__(self, repo):
        self.repo = repo
```

---

### Fluent API

> A style of API design where methods return the object itself, enabling readable method chaining.

```python
obj = Builder().x(1).y(2).build()
```

---

## Summary

* Singleton → one shared instance
* Factory → centralized object creation
* Builder → step-by-step construction
* Adapter → interface translation
* Decorator → add behavior without modifying code
* Facade → simplify complex systems
* Strategy → interchangeable algorithms
* Observer → event-based communication
* Command → action as an object
* DI → inject dependencies from outside
* Fluent API → readable method chaining

---

# Remaining Design Patterns (Not Covered Yet)

## Creational

### Abstract Factory
> Provides an interface for creating families of related objects without specifying their concrete classes.

---

### Prototype
> Creates new objects by copying an existing instance instead of constructing from scratch.

---

## Structural

### Bridge
> Decouples abstraction from implementation so both can vary independently.

---

### Composite
> Treats individual objects and groups of objects uniformly (tree structures).

---

### Flyweight
> Reduces memory usage by sharing common parts of objects.

---

### Proxy
> Provides a placeholder or wrapper to control access to another object (e.g. lazy loading, caching, access control).

---

## Behavioral

### Iterator
> Provides a way to traverse a collection without exposing its internal structure.

---

### Template Method
> Defines the skeleton of an algorithm, allowing subclasses to override specific steps.

---

### State
> Allows an object to change its behavior when its internal state changes.

---

### Visitor
> Lets you add new operations to objects without modifying their classes.

---

### Mediator
> Centralizes communication between objects to reduce direct dependencies.

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
