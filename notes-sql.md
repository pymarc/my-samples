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
