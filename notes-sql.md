# PostgreSQL – Query Planning & Indexes (Practical Notes)

## 1. How PostgreSQL executes queries
PostgreSQL does **not** execute SQL directly.  
It:
1. Parses SQL
2. Builds multiple possible execution plans
3. Estimates cost using statistics
4. Chooses the **cheapest plan**
5. Executes it

The chosen plan is visible via `EXPLAIN ANALYZE`.

---

## 2. `EXPLAIN` vs `EXPLAIN ANALYZE`

```sql
EXPLAIN SELECT ...
````

* shows estimated plan
* does not execute the query

```sql
EXPLAIN ANALYZE SELECT ...
```

* executes the query
* shows **real execution time** and **real row counts**
* always use this when debugging performance

---

## 3. Sequential Scan vs Index Scan

### Sequential Scan (`Seq Scan`)

* Reads the entire table row by row
* Applies filters after reading rows
* Often faster when:

  * table is small
  * large percentage of rows match - e.g. the query will match 30% of all rows

Example output:

```
Seq Scan on users
Filter: (email = ...)
Rows Removed by Filter: 99999
```

---

### Index Scan

* Uses an index to locate matching rows
* Fetches only required rows from the table
* Very fast for highly selective queries - e.g. just one or two rows match it

Example output:

```
Index Scan using users_email_idx
Index Cond: (email = ...)
```

> Index exists ≠ index is used, because sometimes Seq Scan is better performance.

---

## 4. B-tree index (default index type)

* Balanced, ordered tree structure
* Lookup complexity: **O(log N)**
* Default index type in PostgreSQL

```sql
CREATE INDEX ON users (email);
```

### B-tree supports:

* equality (`=`)
* ranges (`<`, `>`, `BETWEEN`)
* `ORDER BY`
* `LIMIT`

### Does NOT work well with:

```sql
LIKE '%something'
```

(leading wildcard breaks ordering)

---

## 5. Selectivity matters

Indexes are most useful when **few rows match**.

* High selectivity → Index Scan
* Low selectivity (10%+ rows) → Seq Scan often faster

PostgreSQL may ignore an index if:

* many rows match
* random I/O is more expensive than sequential scan
* statistics indicate low selectivity

---

## 6. Why `LIKE 'user5%'` used Seq Scan

```sql
WHERE email LIKE 'user5%'
```

* Matches a significant fraction of rows
* Requires fetching many heap pages
* Planner chooses Seq Scan as the cheaper option

This is expected and correct behavior.

---

## 7. ORDER BY + LIMIT = index superpower

Indexes shine when combined with `LIMIT`.

Without index:

```sql
ORDER BY created_at DESC LIMIT 50
```

→ Seq Scan + Sort

With index:

```sql
CREATE INDEX ON users (created_at DESC);
```

→ Index Scan
→ No sort
→ Stops early due to `LIMIT`

---

## 8. Composite (multi-column) indexes

```sql
CREATE INDEX ON users (email, created_at DESC);
```

### Golden rule:

> **Indexes are used left to right.**

This index works for:

* `WHERE email = ...`
* `WHERE email = ... ORDER BY created_at`
* `WHERE email = ... AND created_at > ...`

Does not help for:

```sql
WHERE created_at > ...
```

---

## 9. Index Scan vs Bitmap Index Scan

* **Index Scan**

  * Best when few rows match
  * Direct index → heap lookup

* **Bitmap Index Scan**

  * Used when many rows match
  * Collects row locations first
  * Fetches heap pages in batches
  * Reduces random I/O

Planner selects automatically.

---

## 10. Index-only scan (fastest possible)

Possible when:

* Query selects only indexed columns
* Visibility map allows it

Example:

```sql
SELECT email FROM users WHERE email LIKE 'user5%';
```

Index-only scans avoid touching the table entirely.

---

## 11. Statistics matter

PostgreSQL relies on statistics for planning.

Run manually if needed:

```sql
ANALYZE users;
```

Outdated statistics can lead to poor query plans.

---

## 12. `interval` type (time arithmetic)

`interval` represents a **duration** (similar to Python `timedelta`).

Examples:

```sql
NOW() - interval '7 days'
NOW() - i * interval '1 day'
```

Used for:

* time-based filters
* realistic test data generation
* date arithmetic


# PostgreSQL — Day 2: Data Modeling, Constraints & Foreign Keys (Summary Notes)

## 1. Primary Key (PK) vs Foreign Key (FK)

### Primary Key
- Uniquely identifies a row
- Implicitly `UNIQUE` and `NOT NULL`
- Only one PK per table
- Usually a **surrogate key** (technical ID)

Typical choice:
```sql
id BIGSERIAL PRIMARY KEY
````

### Foreign Key

* Enforces referential integrity between tables
* References a PK (or UNIQUE key) in another table
* FK column type **must match** PK type exactly

```sql
user_id BIGINT REFERENCES users(id)
```

---

## 2. BIGSERIAL / BIGINT — when and why

### Why `BIGSERIAL` for PK

* Backed by `BIGINT` + sequence
* Practically unlimited range (~9e18)
* Avoids painful future migrations
* Negligible performance cost vs `INT`

**Rule of thumb:**

> BIGINT is cheap, migrations are expensive.

### FK type

* Always the same type as PK
* `BIGSERIAL` PK → `BIGINT` FK

### When NOT to use BIGSERIAL

* `UUID` PKs (distributed systems, event-driven)
* Small, guaranteed-limited systems (sometimes `INT`)
* Rare cases of natural keys (lookup tables)

---

## 3. What a Foreign Key actually locks

When inserting a child row:

```sql
INSERT INTO orders (user_id) VALUES (123);
```

PostgreSQL:

* DOES NOT lock the entire parent table
* DOES lock:

  * the **index on users(id)**
  * the **entire parent row** `users(id = 123)`

Important:

* PostgreSQL has **row-level locks, not column-level locks**
* The lock applies to the whole row, not just the `id` column

---

## 4. What operations are affected by FK locks

For parent row `users(id = 123)`:

| Operation                           | Blocked?           |
| ----------------------------------- |--------------------|
| `SELECT`                            | No (MVCC snapshot) |
| `INSERT order(user_id=123)`         | Acquires lock      |
| `UPDATE users SET ... WHERE id=123` | May wait           |
| `DELETE FROM users WHERE id=123`    | Blocked            |

FK checks use a **KEY SHARE** lock to prevent deletion or PK modification.

---

## 5. Why Foreign Keys can be problematic

Foreign Keys are **not free**:

### Costs:

* Extra work on every INSERT / UPDATE / DELETE
* Additional locks and contention
* Reduced write throughput
* Tighter coupling between tables

### Common pain points:

* High write volume systems
* Hot parent rows (many inserts referencing same parent)
* Event / log / audit tables
* Async or eventually consistent systems
* Large cascading deletes

---

## 6. When Foreign Keys ARE a good idea

FKs are recommended when:

* Data correctness is critical
* System is CRUD-style
* Write throughput is moderate
* Strong consistency is required

Examples:

* Orders → Users
* Invoices → Customers
* Payments → Invoices

---

## 7. When Foreign Keys are often avoided

FKs are often skipped intentionally in:

* Event tables
* Log tables
* Audit tables
* Data ingestion pipelines
* High-throughput async systems

In these cases:

* Referential integrity is enforced at application or pipeline level
* Consistency may be eventual, not immediate

---

## 8. Soft delete + FK pattern

Instead of deleting parent rows:

```sql
deleted_at TIMESTAMP NULL
```

Soft delete:

```sql
UPDATE users SET deleted_at = NOW() WHERE id = 123;
```

Keeps FK relationships intact and avoids cascade issues.

---

## 9. Partial indexes with soft delete (important optimization)

If using soft delete, always combine with a partial index:

```sql
CREATE INDEX users_email_active_idx
ON users (email)
WHERE deleted_at IS NULL;
```

Benefits:

* Smaller index
* Faster queries
* Matches real application access pattern

---

## 10. Index on FK column (CRITICAL)

PostgreSQL does **not** automatically index FK columns.

Always add:

```sql
CREATE INDEX orders_user_id_idx ON orders (user_id);
```

Without it:

* DELETE / UPDATE on parent is slow
* FK checks are expensive
* Lock contention increases

---

## 11. Key mental model (important)

> Foreign Key enforcement requires synchronization.
> Synchronization always has a cost.

Therefore:

* FK usage is an **architectural decision**, not a default checkbox.

---

## 12. Interview-ready statements

* "PostgreSQL locks rows, not columns."
* "Foreign keys enforce consistency by acquiring row-level locks."
* "I default to BIGSERIAL/BIGINT to avoid future migrations."
* "Foreign keys are great, but not free—especially under high write load."
* "Soft deletes combined with partial indexes are a common production pattern."

---

## 13. Decision cheat sheet

| Scenario                      | Use FK |
| ----------------------------- |--------|
| CRUD app, business data       | OK     |
| Billing / financial data      | OK     |
| Event / log tables            | X      |
| High write throughput         | X      |
| Async / eventual consistency  | X      |
| Data ingestion / ML pipelines | X      |

---

## 14. One-sentence summary

> Foreign keys provide strong consistency via row-level locking, but introduce write overhead and coupling, so they should be used deliberately rather than by default.


# PostgreSQL — Day 3: Transactions, Locks & Isolation (Summary Notes)

## 1. Transactions basics
A transaction groups multiple SQL statements into an atomic unit:
- all statements succeed → `COMMIT`
- any statement fails → `ROLLBACK`

```sql
BEGIN;
-- SQL statements
COMMIT;
````

If an error occurs:

```sql
ROLLBACK;
```

---

## 2. Aborted transaction state (CRITICAL)

If **any statement inside a transaction fails**:

* the entire transaction enters **aborted state**
* PostgreSQL ignores all further commands
* error code: `SQLSTATE 25P02`

Only way to recover:

```sql
ROLLBACK;
```

> After the first error, nothing runs until you rollback.

This applies equally to:

* pgAdmin
* psql
* backend applications
* ORMs

---

## 3. MVCC (Multi-Version Concurrency Control)

PostgreSQL uses MVCC:

* `SELECT` does not block `UPDATE`
* readers see a consistent snapshot
* writers create new row versions

---

## 4. Isolation levels (practical meaning)

### READ COMMITTED (default)

* each statement sees latest committed data
* same `SELECT` may return different results in one transaction
* allows non-repeatable reads

Use for:

* typical CRUD
* most API endpoints

---

### REPEATABLE READ

* snapshot taken at transaction start
* all reads see the same data
* prevents non-repeatable reads
* still allows write skew

Use for:

* reports
* multi-step read logic
* stable view of data

---

### SERIALIZABLE

* guarantees serial execution effect
* prevents write skew
* may abort transactions with `serialization_failure`
* requires retry logic

Use for:

* critical business invariants
* complex concurrent logic

---

## 5. Row-level locking

PostgreSQL locks **rows, not columns**.

### `UPDATE`

* implicitly acquires a `FOR UPDATE` row lock

### `SELECT ... FOR UPDATE`

* explicitly locks selected rows
* blocks other updates and deletes
* does not block plain SELECTs

```sql
SELECT * FROM users WHERE id = 1 FOR UPDATE;
```

---

## 6. When to use SELECT FOR UPDATE

### Not needed when:

```sql
UPDATE users SET email='x' WHERE id=1;
```

### Needed when:

* read → decide → write pattern
* preventing lost updates

```sql
BEGIN;
SELECT balance FROM accounts WHERE id=1 FOR UPDATE;
UPDATE accounts SET balance = balance - 10 WHERE id=1;
COMMIT;
```

---

## 7. Foreign Keys and locks (recap)

* FK checks acquire `KEY SHARE` locks on parent rows
* parent row is locked, not the whole table
* high concurrency + FK can cause lock contention

---

## 8. Deadlocks

Deadlocks occur when transactions lock resources in different orders.

PostgreSQL:

* detects deadlocks automatically
* aborts one transaction

Avoid by:

* consistent lock ordering
* short transactions
* minimal locking

---

## 9. Backend rule of thumb

> Always rollback on error before reusing a connection.

---

## 10. One-sentence takeaway

> Isolation levels define how stable your view of data is during a transaction, while row-level locks define who is allowed to modify data concurrently.


# Day 4 – PostgreSQL: JSONB, Event Tables & GIN Indexes

## JSON vs JSONB

### JSON
- Stored as text
- Parsed on every read
- Slow to query
- Rarely used in practice

### JSONB (recommended)
- Binary format
- Parsed on write
- Fast to query
- Supports indexing (GIN)

**Rule:** If you store JSON in PostgreSQL → always use `JSONB`.

---

## Basic JSONB operators

Assuming column `data JSONB`:

- Access field:
  ```sql
  data -> 'status'
````

* Access field as text:

  ```sql
  data ->> 'status'
  ```
* Nested access:

  ```sql
  data -> 'user' ->> 'email'
  ```
* Containment (most common):

  ```sql
  data @> '{"status":"error"}'
  ```

---

## Event table pattern

Event tables are typically:

* Append-only
* Schema-flexible
* Optimized for writes and reads, not strict relations

Example:

```sql
CREATE TABLE user_event (
    id BIGSERIAL PRIMARY KEY,
    user_name TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK (event_type IN ('general', 'error')),
    data JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Key design decisions

* No foreign keys (intentional, for performance)
* `JSONB` for flexible payload
* `TIMESTAMPTZ` for correct time handling (UTC)
* `CHECK` instead of ENUM for easier evolution

---

## TIMESTAMP vs TIMESTAMPTZ

* `TIMESTAMP` → **not timezone-aware**
* `TIMESTAMPTZ` → stores an absolute moment in time (internally UTC)

**Best practice for backend/event tables:**

```sql
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

---

## Indexing strategy for event tables

### Why multiple indexes may be needed

Different queries have different access patterns. One index rarely fits all.

---

### Index for per-user latest events (most common)

```sql
CREATE INDEX user_event_user_created_idx
ON user_event (user_name, created_at DESC);
```

Optimized for:

```sql
WHERE user_name = ?
ORDER BY created_at DESC
LIMIT N;
```

---

### Index for global latest events (optional)

```sql
CREATE INDEX user_event_created_idx
ON user_event (created_at DESC);
```

Optimized for:

```sql
ORDER BY created_at DESC
LIMIT N;
```

---

## Why `DESC` in indexes matters

* Index direction should match the most common `ORDER BY`
* `created_at DESC` is ideal for “latest events” queries
* PostgreSQL *can* scan indexes backwards, but not always optimally

**Rule:** Design indexes for the most common `ORDER BY + LIMIT`.

---

## GIN index on JSONB

### What GIN does

* GIN = **inverted index**
* Indexes all keys and values inside JSONB
* Excellent for containment queries (`@>`, `?`)

Example:

```sql
CREATE INDEX user_event_data_gin_idx
ON user_event USING GIN (data);
```

---

### Downsides of full GIN on JSONB

* Large index size
* Slower INSERT/UPDATE
* High maintenance cost

---

### When full GIN makes sense

* Many different JSON fields queried
* Unknown query patterns
* Moderate write throughput

---

### Better alternatives (often preferred)

#### 1. Extract frequently queried fields to columns

```sql
status TEXT,
data JSONB
```

#### 2. Partial GIN index

```sql
CREATE INDEX user_event_error_data_gin_idx
ON user_event USING GIN (data)
WHERE event_type = 'error';
```

#### 3. Expression index

```sql
CREATE INDEX user_event_status_idx
ON user_event ((data ->> 'status'));
```

