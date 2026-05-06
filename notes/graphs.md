# Graphs Cheat Sheet

## Core Concepts

* Graph = nodes + edges
* Types:

  * **Directed / Undirected**
  * **Weighted / Unweighted**
* Representation:

```python
# Adjacency list
graph = {
    0: [1, 2],
    1: [2],
    2: []
}
```

---

# BFS (Breadth-First Search)

## Use when:

* shortest path in **unweighted graph**
* level-by-level traversal
* “minimum steps”, “fewest moves”

## Template

```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])

    while queue:
        node = queue.popleft()

        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                queue.append(nei)
```

---

## Shortest Path (with parents)

```python
def bfs_shortest_path(graph, start):
    from collections import deque

    queue = deque([start])
    parents = {start: None}

    while queue:
        node = queue.popleft()

        for nei in graph[node]:
            if nei not in parents:
                parents[nei] = node
                queue.append(nei)

    return parents
```

---

## Reconstruct Path

```python
def build_path(parents, target):
    if target not in parents:
        return None

    path = []
    while target is not None:
        path.append(target)
        target = parents[target]

    return path[::-1]
```

---

# Multi-source BFS

## Use when:

* spread over time (fire, infection, signal)

## Template

```python
from collections import deque

def multi_source_bfs(starts):
    queue = deque(starts)
    steps = 0

    while queue:
        for _ in range(len(queue)):
            node = queue.popleft()
            # process

        steps += 1
```

---

# DFS (Depth-First Search)

## Use when:

* explore all paths
* components
* cycle detection

## Iterative

```python
def dfs(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)

        for nei in graph[node]:
            stack.append(nei)

    return visited
```

---

## Cycle Detection (Undirected)

```python
def has_cycle(graph):
    visited = set()

    for start in graph:
        if start in visited:
            continue

        stack = [(start, None)]

        while stack:
            node, parent = stack.pop()

            if node in visited:
                continue

            visited.add(node)

            for nei in graph[node]:
                if nei not in visited:
                    stack.append((nei, node))
                elif nei != parent:
                    return True

    return False
```

---

# Grid = Graph

## Moves:

```python
dirs = [(1,0), (-1,0), (0,1), (0,-1)]
```

## Bounds check:

```python
0 <= r < rows and 0 <= c < cols
```

---

# Number of Islands (DFS)

```python
def num_islands(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()

    def dfs(r, c):
        stack = [(r,c)]
        while stack:
            r, c = stack.pop()

            if not (0 <= r < rows and 0 <= c < cols):
                continue
            if grid[r][c] == "0" or (r,c) in visited:
                continue

            visited.add((r,c))

            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                stack.append((r+dr, c+dc))

    count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r,c) not in visited:
                dfs(r,c)
                count += 1

    return count
```

---

# Topological Sort (BFS / Kahn)

## Use when:

* dependencies
* ordering tasks

## Template

```python
from collections import deque

def topo_sort(graph):
    indegree = {node: 0 for node in graph}

    for node in graph:
        for nei in graph[node]:
            indegree[nei] += 1

    queue = deque([n for n in graph if indegree[n] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)

    if len(result) != len(graph):
        return None  # cycle

    return result
```

---

# Dijkstra (Weighted Graph)

## Use when:

* shortest path with weights ≥ 0

## Template

```python
import heapq

def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0

    heap = [(0, start)]

    while heap:
        cur_dist, node = heapq.heappop(heap)

        if cur_dist > dist[node]:
            continue

        for nei, w in graph[node]:
            new_dist = cur_dist + w

            if new_dist < dist[nei]:
                dist[nei] = new_dist
                heapq.heappush(heap, (new_dist, nei))

    return dist
```

---

## Early Exit

```python
if node == target:
    return cur_dist
```

---

# 🔗 Union-Find (Disjoint Set)

## Use when:

* components
* connectivity
* cycle detection (undirected)

---

## Template

```python
def count_components(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        root_a = find(a)
        root_b = find(b)

        if root_a != root_b:
            parent[root_b] = root_a

    for u, v in edges:
        union(u, v)

    roots = set(find(i) for i in range(n))
    return len(roots)
```

---

# Decision Guide

| Problem                    | Use        |
| -------------------------- | ---------- |
| shortest path (unweighted) | BFS        |
| shortest path (weighted)   | Dijkstra   |
| traversal / components     | DFS        |
| grid problems              | DFS/BFS    |
| dependencies               | Topo sort  |
| connectivity / groups      | Union-Find |
| cycle (undirected)         | Union-Find |

---

# Key Insights

* BFS = **levels / time / shortest path**
* DFS = **exploration**
* Dijkstra = **cheapest path first**
* Topo = **dependency order**
* Union-Find = **group tracking**

---

# One-liners

* BFS → *minimum steps*
* DFS → *explore everything*
* Dijkstra → *cheapest path*
* Topo → *order with constraints*
* Union-Find → *who is connected*
