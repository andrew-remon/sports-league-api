# Subquery Mental Model

## 1. How to break down a complex query into steps
* Define each operation as a single statement.
* Define the tables needed for each operation.
* Identify what each subquery should return *(a scalar, a list, or a table)*
* Write the query from the inner (subqueries) to the most outer ones.
* Test each level to check the fetching correctness then proceed to the next outer one.

## 2. How to decide between a subquery and a JOIN
In most cases, JOIN have a better performance than a subquery. However, with more complex statements and use_cases, subquery provide a powerful tool to fetch the most detailed information (filtered aggregation).
So overall, JOIN + GROUP BY → when you want to display aggregated data alongside other columns,
Subquery → when you need to filter or compare against an aggregated value (e.g., WHERE salary > (SELECT AVG(salary) FROM employees))

## 3. How to test a subquery independently before embedding it
First test the output data of this subquery to compare it against intended one.
Next, Run EXPLAIN ANALYZE over the subquery to analyze its efficieny and step by step process.

---
---

## Practice

### Q1: Count of players per team, ordered by count descending (aggregation)

**SQL**:
--------
SELECT t.name, count(p.first_name) AS players_counter
FROM leagues_team t
JOIN leagues_player p
ON t.id = p.team_id
GROUP BY t.name
ORDER BY players_counter desc;

**ORM**:
--------
Team.objects.annotate(players_count=Count('players')).values('name','players_count')


**Generated SQL**:
------------------
SELECT "leagues_team"."name" AS "name", COUNT("leagues_player"."id") AS "players_count" FROM "leagues_team" LEFT OUTER JOIN "leagues_player" ON ("leagues_team"."id" = "leagues_player"."team_id") GROUP BY "leagues_team"."id"

---

 ## Q2: Teams that have no players (LEFT JOIN + NULL check, or subquery)

**SQL**:
--------
*(1)*
SELECT t.name
FROM leagues_team t
LEFT JOIN leagues_player p
ON t.id = p.team_id
GROUP BY t.name
HAVING count(p.first_name) = 0;

or

SELECT t.name
FROM leagues_team t
LEFT JOIN leagues_player p
ON t.id = p.team_id
where p.team_id IS NUll;


*(2)*
SELECT t.name
FROM leagues_team t
WHERE t.id NOT IN(
    SELECT p.team_id
    FROM leagues_player p
);

**ORM**:
--------
Team.objects.annotate(players_count=Count('players')).filter(players_count = 0).values('name')

**Generated SQL**:
------------------
SELECT "leagues_team"."name" AS "name" FROM "leagues_team" LEFT OUTER JOIN "leagues_player" ON ("leagues_team"."id" = "leagues_player"."team_id") GROUP BY "leagues_team"."id" HAVING COUNT("leagues_player"."id") = 0

---

## Q3: Players whose team is in the league named "Premier League" (subquery or JOIN)

**SQL**:
--------
*(1)*
SELECT CONCAT(p.first_name, ' ', p.last_name) AS player_name
FROM leagues_player p
JOIN leagues_team t
ON t.id = p.team_id
JOIN leagues_league l
ON l.id = t.league_id
WHERE l.name = 'Premier League';

*(2)*

SELECT CONCAT(p.first_name, ' ', p.last_name) AS player_name
FROM leagues_player p
WHERE p.team_id IN (
    SELECT t.id
    FROM leagues_team t
    JOIN leagues_league l
    ON l.id = t.league_id
    WHERE l.name = 'Premier League'
);

**ORM**:
--------

english_teams = Team.objects.filter(league__name='Premier League')
english_teams_id = set(english_teams.values_list('id', flat=True))
Player.objects.filter(team__id__in=english_teams_id)

**Generated SQL**:
------------------
SELECT "leagues_player"."id", "leagues_player"."first_name", "leagues_player"."last_name", "leagues_player"."team_id", "leagues_player"."jersey_number", "leagues_player"."position", "leagues_player"."date_of_birth", "leagues_player"."created_at" FROM "leagues_player" WHERE "leagues_player"."team_id" IN (8, 3, 4, 5)


---

## Q4: The team with the most players (subquery with MAX)

**SQL**:
--------
*with claude help...*
SELECT t.name, COUNT(p.first_name) AS players_count
FROM leagues_team t
JOIN leagues_player p
ON t.id = p.team_id
GROUP BY t.name
HAVING COUNT(p.first_name) = (
    SELECT MAX(player_count)
    FROM (
        SELECT COUNT(p2.first_name) AS player_count
        FROM leagues_team t2
        JOIN leagues_player p2 ON t2.id = p2.team_id
        GROUP BY t2.name
    )
);


**ORM**:
--------
max_count = Team.objects.annotate(players_count=Count('players')).aggregate(max=Max('players_count'))['max']
Team.objects.annotate(players_count=Count('players')).filter(players_count=max_count).values('name', 'players_count')

**Generated SQL**:
------------------
SELECT "leagues_team"."name" AS "name", COUNT("leagues_player"."id") AS "players_count" FROM "leagues_team" LEFT OUTER JOIN "leagues_player" ON ("leagues_team"."id" = "leagues_player"."team_id") GROUP BY "leagues_team"."id" HAVING COUNT("leagues_player"."id") = 3

---

## Q5: Average number of players per team across all leagues (subquery)

**SQL**:
--------
SELECT AVG(player_count_per_team)
FROM (
    SELECT t.name, COUNT(p.first_name) AS player_count_per_team
    from leagues_team t
    JOIN leagues_player p
    ON t.id = p.team_id
    GROUP BY t.name
) AS team_stats;


**ORM**:
--------
Team.objects.annotate(player_count=Count('players')).filter(player_count__gt=0).aggregate(average=Avg('player_count'))['average']

---

## Q6: Teams where player count is above the league's average player count per team (correlated subquery)

**SQL**:
--------
SELECT t2.name
FROM leagues_team t2
JOIN leagues_player p2
ON t2.id = p2.team_id
GROUP BY t2.name, t2.league_id -- we include t2.team_id because it's correlated in the inner query
HAVING COUNT(p2.first_name) > (
    SELECT CAST(COUNT(p.first_name) as float)/COUNT(Distinct t.name) -- using casting
    FROM leagues_team t
    JOIN leagues_player p
    ON t.id = p.team_id
    JOIN leagues_league l
    ON l.id = t.league_id
    where t2.league_id = l.id
);

or

SELECT t2.name
FROM leagues_team t2
JOIN leagues_player p2 ON t2.id = p2.team_id
GROUP BY t2.name, t2.league_id, t2.id
HAVING COUNT(p2.first_name) > (
    SELECT AVG(team_player_counts.player_count)
    FROM (
        SELECT COUNT(p.id) AS player_count
        FROM leagues_team t
        JOIN leagues_player p ON t.id = p.team_id
        WHERE t.league_id = t2.league_id
        GROUP BY t.id
    ) AS team_player_counts
);


**ORM**:
--------
*Using Antigravity help*

player_count_per_team = Team.objects.annotate(player_count=Count('players'))

league_average_subquery = Team.objects.filter(
    league=OuterRef('league')
).values(
    # 1. Group by league
    'league'
).annotate(
    # 2. Divide total players (cast to float) by count of distinct teams
    avg_players=Cast(Count('players'), FloatField()) / Count('id', distinct=True)
).values(
    # 3. Select only the calculated average
    'avg_players'
)


result = player_count_per_team.filter(
    player_count__gt=Subquery(league_average_subquery)
)

**Generated SQL**:
------------------
SELECT "leagues_team"."id", "leagues_team"."name", "leagues_team"."league_id", "leagues_team"."founded_year", "leagues_team"."city", "leagues_team"."created_at", "leagues_team"."updated_at", COUNT("leagues_player"."id") AS "player_count" FROM "leagues_team" LEFT OUTER JOIN "leagues_player" ON ("leagues_team"."id" = "leagues_player"."team_id") GROUP BY "leagues_team"."id", "leagues_team"."league_id" HAVING COUNT("leagues_player"."id") > (SELECT ((COUNT(U2."id"))::double precision / COUNT(DISTINCT U0."id")) AS "avg_players" FROM "leagues_team" U0 LEFT OUTER JOIN "leagues_player" U2 ON (U0."id" = U2."team_id") WHERE U0."league_id" = ("leagues_team"."league_id") GROUP BY U0."league_id")
