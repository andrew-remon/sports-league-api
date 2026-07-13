## 1. File Naming

```text
test_<concept>.py or
test_<model>.py
```

## 2. Test Naming

```text
test_<action>_<scenario>
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
