# Phase 1 Summary

## What Worked

### 1. I could stick to plan

Day by day, finishing what's required, when got a time-bottleneck, I recovered and compensate it the next day.

### 2. Documentation ease

Before the beginning of this phase, the fact that I could check the documentation of any concept to learn or revise it was a nightmare. Today, I easily check and read and fight to understand using documentation.

### 3. I understand what I am coding

It wasn't a copy-paste phase, it was a journey of learning and applying (with understanding - even if not full) through the project, I have a grasp of what's the request/response lifecyle (Network and Django wise), how urls root views which interact with serializers, I am now more confident dealing with GitHub commands (better branch-naming conventions, best-practice commits strategy), I actually know different tools like curl, black, flake8, etc...

---

## What didn't work

### 1. Linux Pipes

It's actually harder to create sequential linux commands like `lego` puzzle, it's not intuitive for me till now, it's an area of linux-journey improvement

### 2. Direct immersion in views, serializers, urls (last week in phase 1)

For a beginner who just starts discovering backend, it was too much to understand at first time, I needed to dedicate a full day to just link the dots and understand the code and how it goes like this, for example: why do we override `get_queryset()` to add `select_related()` or `prefetch_related()`, why using many=true in serializers definition in views, dispatch() role in request lifecyle in DRF.

### 3. Me

There's no cause to get of schedule or hit my determination (except for trips, urgencies), throughout this phase's journey, sometimes, I feel like I didn't wan't to continue. Fighting with myself was the hardest thing I encounter.

---

## Biggest Surprise
Backend isn't just series of requests and responses. It's about request, response, avoiding too much DB hits (aware of N+1 issue), performance, query optimization. Backend highlights the fact that resources (DB, bandwidth, storage, buffer) are limited and when the data become large and server got too many requests, the application should be ready and armed with what I mention earlier.

---

## Skills Gap

- Project Structure Awareness
I need to better grasp the project structure, how for example to create seed_data.py (by creating a command folder and __init__.py file, overriding Command class), how to create unit tests and I mean here syntactic-wise grasp.

---

## Project status

### Project can
- Get a list of leagues, teams, players
- Get a list of teams per league
- Get a list of players per team
- Get standings of a league
- Create a league, team, player, match
- Create a result for a match
- Update/Delete league, team, player, match

### Project can't
- Update a match result

