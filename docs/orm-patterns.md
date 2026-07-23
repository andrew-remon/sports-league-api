# A reference document with code examples for 6 ORM patterns

## 1. Atomic Counter

* **explanation:** increment a field without loading the object (F expression)

* **ORM:**
```python
from leagues.models import MatchResult
from django.db.models import F

specific_match_result = MatchResult.objects.get(pk=4) # must ensure that this match is already COMPLETED or IN_PROGRESS
specific_match_result.home_score = F("home_score") + 2
specific_match_result.save()

# or using
# MatchResult.objects.filter(pk=4).update(home_score=F("home_score") + 2)
```

* **SQL:**
```sql
UPDATE "leagues_matchresult"
SET "home_score" = ("leagues_matchresult"."home_score" + 2)
WHERE "leagues_matchresult"."id" = 4;
```
---

## 2. Cross-field filter

* **explanation:**  find records where one field is greater than another (F expression)

* **ORM:**
```python
from leagues.models import MatchResult
from django.db.models import F

home_teams_win = MatchResult.objects.filter(home_score__gt=F("away_score"))
```

* **SQL:**
```sql
SELECT *
FROM "leagues_matchresult"
WHERE "leagues_matchresult"."home_score" > ("leagues_matchresult"."away_score");
```

---

## 3. Annotate with subquery

* **explanation:** attach a value from a related table (Subquery + OuterRef)


* **ORM:**
```python
from leagues.models import League, Match
from django.db.models import Subquery, OuterRef

# annotate each league with its latest match date.
latest_match_date = Match.objects.filter(league=OuterRef("pk")).order_by("-scheduled_date").values("scheduled_date")[:1]
League.objects.annotate(latest_match_date=Subquery(latest_match_date))
```

* **SQL:**
```sql
SELECT *
       (SELECT U0."scheduled_date"
        FROM "leagues_match" U0
        WHERE U0."league_id" = ("leagues_league"."id")
        ORDER BY U0."scheduled_date" DESC
        LIMIT 1) AS "latest_match_date"
FROM "leagues_league";
```
---

## 4. Existense check

* **explanation:**  filter records that have/don't have related objects (Exists)

* **ORM:**
```python
from django.db.models import Exists, OuterRef
from leagues.models import Match, MatchResult

# Retrieve matches which have results
results = MatchResult.objects.filter(match=OuterRef("pk"))
Match.objects.annotate(is_played=Exists(results))
```

* **SQL:**
```sql
SELECT *
       EXISTS(
           SELECT 1 AS "a"
           FROM "leagues_matchresult" U0
           WHERE U0."match_id" = ("leagues_match"."id")
           LIMIT 1
       ) AS "is_played"
FROM "leagues_match";
```

---

## 5. Date grouping

* **explanation:** group results by month or year (TruncMonth + annotate)

* **ORM:**
```python
from django.db.models import Count
from django.db.models.functions import TruncMonth

# count the number or leagues created per month
League.objects.annotate(month=TruncMonth("created_at")).values("month").annotate(league_count=Count("pk")).order_by("month")
```

* **SQL:**
```sql
SELECT DATE_TRUNC('month', "leagues_league"."created_at" AT TIME ZONE 'UTC') AS "month",
       COUNT("leagues_league"."id") AS "league_count"
FROM "leagues_league"
GROUP BY DATE_TRUNC('month', "leagues_league"."created_at" AT TIME ZONE 'UTC')
ORDER BY "month" ASC;
```

---

## 6. Ranking

* **explanation:** rank records within a group (Window + DenseRank)

* **ORM:**
```python
# defined in services.py, last two code chunks
```

* **SQL:**
```sql
SELECT "leagues_team"."name",
       "points",
       "goal_difference",
       "goals_for",
       DENSE_RANK() OVER (
           ORDER BY "points" DESC, "goal_difference" DESC, "goals_for" DESC
       ) AS "rank"
FROM "leagues_team"
ORDER BY "rank" ASC;
```
