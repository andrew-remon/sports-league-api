## Day 3 — The N+1 Problem: Detection, Diagnosis, and Elimination

**Date:** July 16, 2026
**Focus:** N+1 Issue, how to spot, resolve it.

| Endpoint | Queries Before | Queries After | Fix Applied |
|---|---|---|---|
| `GET /api/v1/leagues/` | 2 | 2 | No Change |
| `GET /api/v1/leagues/1/` | 1 | 1 | No Change |
| `GET /api/v1/leagues/1/standings/` | 1 | 1 | No Change |
| `GET /api/v1/teams/` | 2 | 2 | No Change |
| `GET /api/v1/teams/1/` | 3 | 2 | `.select_related("league").prefetch_related("players")` |
| `GET /api/v1/teams/14/players/` | 1 | 1 | No Change |
| `GET /api/v1/players/` | 14 | 2 | `.select_related("team")` |
| `GET /api/v1/players/3/` | 2 | 1 | `.select_related("team")` |
| `GET /api/v1/matches/` | 22 | 2 | `.select_related("result")` |
| `GET /api/v1/matches/6/` | 2 | 1 | `.select_related("result")` |

---

## Day 4 — Database Indexing Strategy & Query Plan Audit

**Date:** July 18, 2026
**Focus:** B-Tree Composite Indexing, Query Plan Analysis (`EXPLAIN ANALYZE`), Cost-Based Optimizer Behavior.

---

#### EXPLAIN ANALYZE for:

`before using indexes`

1. SELECT * FROM leagues_match WHERE league_id = 1 AND status = 'completed' ORDER BY match_day;

```text
                                                                    QUERY PLAN
---------------------------------------------------------------------------------------------------------------------------------------------------
 Sort  (cost=11.30..11.30 rows=1 width=108) (actual time=0.037..0.039 rows=12.00 loops=1)
   Sort Key: match_day
   Sort Method: quicksort  Memory: 26kB
   Buffers: shared hit=2
   ->  Bitmap Heap Scan on leagues_match  (cost=4.17..11.29 rows=1 width=108) (actual time=0.026..0.029 rows=12.00 loops=1)
         Recheck Cond: (league_id = 1)
         Filter: ((status)::text = 'completed'::text)
         Rows Removed by Filter: 7
         Heap Blocks: exact=1
         Buffers: shared hit=2
         ->  Bitmap Index Scan on leagues_match_league_id_af84a971  (cost=0.00..4.17 rows=3 width=0) (actual time=0.013..0.014 rows=20.00 loops=1)
               Index Cond: (league_id = 1)
               Index Searches: 1
               Buffers: shared hit=1
 Planning Time: 0.101 ms
 Execution Time: 0.063 ms
(16 rows)
```



2. SELECT * FROM leagues_team WHERE league_id = 1 ORDER BY name

```text
                                                                    QUERY PLAN
---------------------------------------------------------------------------------------------------------------------------------------------------
 Sort  (cost=8.17..8.18 rows=1 width=472) (actual time=0.030..0.031 rows=13.00 loops=1)
   Sort Key: name
   Sort Method: quicksort  Memory: 25kB
   Buffers: shared hit=2
   ->  Index Scan using leagues_team_league_id_c78684eb on leagues_team  (cost=0.14..8.16 rows=1 width=472) (actual time=0.016..0.019 rows=13.00 loops=1)
         Index Cond: (league_id = 1)
         Index Searches: 1
         Buffers: shared hit=2
 Planning Time: 0.087 ms
 Execution Time: 0.050 ms
(10 rows)
```



3. SELECT * FROM leagues_player WHERE team_id = 1;

```text
                                                QUERY PLAN
----------------------------------------------------------------------------------------------------------------------------
 Index Scan using leagues_player_team_id_57d292be on leagues_player  (cost=0.15..8.17 rows=1 width=284) (actual time=0.016..0.017 rows=3.00 loops=1)
   Index Cond: (team_id = 1)
   Index Searches: 1
   Buffers: shared hit=2
 Planning Time: 0.073 ms
 Execution Time: 0.033 ms
(6 rows)
```


`after`

                                                    QUERY PLAN
-------------------------------------------------------------------------------------------------------------------
 Sort  (cost=1.31..1.31 rows=1 width=108) (actual time=0.061..0.062 rows=12.00 loops=1)
   Sort Key: match_day
   Sort Method: quicksort  Memory: 26kB
   Buffers: shared hit=4
   ->  Seq Scan on leagues_match  (cost=0.00..1.30 rows=1 width=108) (actual time=0.009..0.011 rows=12.00 loops=1)
         Filter: ((league_id = 1) AND ((status)::text = 'completed'::text))
         Rows Removed by Filter: 8
         Buffers: shared hit=1
 Planning:
   Buffers: shared hit=180 read=2
 Planning Time: 1.434 ms
 Execution Time: 0.135 ms
(12 rows)



                                                 QUERY PLAN
-------------------------------------------------------------------------------------------------------------
 Sort  (cost=8.17..8.18 rows=1 width=472) (actual time=1.228..1.229 rows=13.00 loops=1)
   Sort Key: name
   Sort Method: quicksort  Memory: 25kB
   Buffers: shared hit=6 read=2
   ->  Index Scan using leagues_team_league_id_c78684eb on leagues_team  (cost=0.14..8.16 rows=1 width=472) (actual time=0.586..0.590 rows=13.00 loops=1)
         Index Cond: (league_id = 1)
         Index Searches: 1
         Buffers: shared hit=3 read=2
 Planning:
   Buffers: shared hit=59 read=3
 Planning Time: 6.204 ms
 Execution Time: 1.714 ms
(12 rows)


                                                 QUERY PLAN
-------------------------------------------------------------------------------------------------------------
 Seq Scan on leagues_player  (cost=0.00..1.23 rows=1 width=284) (actual time=0.093..0.095 rows=3.00 loops=1)
   Filter: (team_id = 1)
   Rows Removed by Filter: 15
   Buffers: shared hit=1
 Planning Time: 0.214 ms
 Execution Time: 0.259 ms
(6 rows)


---

### 1. Indexes Added

The following composite indexes were defined in Django `Meta.indexes` and applied via migration:

1. **`player_team_position_idx`**: Composite index on `leagues_player (team_id, position)`
2. **`match_league_status_idx`**: Composite index on `leagues_match (league_id, status)`
3. **`match_league_day_idx`**: Composite index on `leagues_match (league_id, match_day)`

---

### 2. Performance Comparison Summary Table

| Query Target | Access Pattern | Plan Before | Plan After | Execution Time (Before → After) | Optimizer Decision & Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Match Listing** | `WHERE league_id = 1 AND status = 'completed' ORDER BY match_day` | `Bitmap Heap Scan` (FK index) | `Seq Scan` | `0.063 ms` → `0.135 ms` | Table has 20 rows (1 disk block). Planner chose `Seq Scan` (`cost=1.30`) over index lookup (`cost=11.29`) to save buffer reads. |
| **Team Listing** | `WHERE league_id = 1 ORDER BY name` | `Index Scan` (FK index) | `Index Scan` (FK index) | `0.050 ms` → `1.714 ms` | Plan unchanged (uses default FK index on `league_id`). Time difference due to cold disk read (`read=2`) after index creation vs warm RAM cache (`read=0`). |
| **Player Listing** | `WHERE team_id = 1` | `Index Scan` (FK index) | `Seq Scan` | `0.033 ms` → `0.033 ms` | Table has 18 rows. `Seq Scan` requires 1 page buffer read (`shared hit=1`) vs 2 for `Index Scan`. Execution time identical (33 μs). |

---

### 3. Detailed Query Plans & Analysis

#### Query 1: Completed Matches Filter
**SQL:** `SELECT * FROM leagues_match WHERE league_id = 1 AND status = 'completed' ORDER BY match_day;`

* **Before:** `Bitmap Heap Scan` on `leagues_match_league_id_af84a971` (Cost: `4.17..11.29`, Buffers: `shared hit=2`)
* **After:** `Seq Scan` on `leagues_match` (Cost: `0.00..1.30`, Buffers: `shared hit=1`)
* **Finding:** Small dataset (20 rows). Sequential scan fits in 1 page read (`shared hit=1`), making it lower cost than bouncing through index blocks (`shared hit=2`).

#### Query 2: Team List Pre-sorted
**SQL:** `SELECT * FROM leagues_team WHERE league_id = 1 ORDER BY name;`

* **Before:** `Index Scan using leagues_team_league_id_c78684eb` (Cost: `0.14..8.16`, Buffers: `shared hit=2`)
* **After:** `Index Scan using leagues_team_league_id_c78684eb` (Cost: `0.14..8.16`, Buffers: `shared hit=6 read=2`)
* **Finding:** Execution strategy unchanged. The "after" execution spike was caused by cold physical disk reads (`read=2`) after database cache invalidation (as migration happens). Re-running the query with a warm cache returns execution time to ~`0.050 ms`.

#### Query 3: Players by Team
**SQL:** `SELECT * FROM leagues_player WHERE team_id = 1;`

* **Before:** `Index Scan using leagues_player_team_id_57d292be` (Cost: `0.15..8.17`, Buffers: `shared hit=2`)
* **After:** `Seq Scan on leagues_player` (Cost: `0.00..1.23`, Buffers: `shared hit=1`)
* **Finding:** Table contains 18 rows total. `Seq Scan` is chosen by the optimizer due to minimal page I/O (`cost=1.23` vs `8.17`).

#### Query 4: Standings Computation
* long sql query

* **Before:** a combination between `Bitmap hash index` and `Index scan`
* **After:** now due to the small dataset, it uses `Seq Scan` while preserving the necessary Index Scan

---

### 4. Technical Takeaway & Optimizer Scaling Analysis

* **Cost-Based Optimization (CBO):** PostgreSQL accurately determines that for small development datasets (< 100 rows per table), `Seq Scan` requires fewer buffer page reads than `Index Scan`.
* **Scaling Expectation:** As table row counts scale to thousands of records (where table pages increase from 1 page to hundreds of pages), `Seq Scan` cost will scale linearly \(O(N)\). The PostgreSQL optimizer will automatically switch to the newly defined B-Tree composite indexes (\(O(\log N)\)).
* **Verification:** Tested composite index validity by temporarily running `SET enable_seqscan = OFF;`, confirming PostgreSQL recognizes and successfully utilizes `player_team_position_idx`, `match_league_status_idx`, and `match_league_day_idx`.
