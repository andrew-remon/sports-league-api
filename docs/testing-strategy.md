## 1. File Naming

```text
test_<concept>.py or
test_<model>.py
```

## 2. Test Naming

```text
test_<entity>_<action>_<scenario>
```

## 3. Fixture Usage Rules

Fixtures got defined when they are repeated across many unit tests (like sample_league, sample_team), However, if we need to just define a helper instance in a specific unit test, then inline setup is better.

## 4. What to assert
- status code
- data correctness
- response structure (sometimes) → check the response is a List for example

## 5. One hard test and why
It's `test_update_league`
It's hard because it needs certain level of dealing with different data (sample_league, data variable and response.data), then checking data variable with response.data and never forget eventually to refresh_from_db().

## 6. Test Categories
Model, Serializer, Permission → Unit tests
View → Integration tests

## 7.Test Data Strategy
for User authentication: Use factories.
for different leagues, matches, players: Use Fixtures.
for results or any on-the-go data: use inline.

## 8. Coverage Goals
Every endpoint must have a happy path test
Every serializer must have a validation failure test
Every permission class must test authorized vs. unauthorized access
Edge cases and error paths are optional unless they involve security or data integrity

## 9. What you won't test
- Django Admin Views
- Middlewares
- Models attributes data type (e.g. League name is varchar)
- Admin/Browsable API


## 10. CI Integration
"The project currently has no external dependencies (no third-party APIs, no email
services, no async tasks). When external calls are introduced, we will mock them using `unittest.mock.patch` to keep tests isolated and fast."
