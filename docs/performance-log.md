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
