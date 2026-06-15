# A 5-rule Error Handling Strategy for the project.


### 1. When to Raise vs Return

Raise is used whenever we need to inform the caller (other function or query) that we cannot proceed in the flow of operations whenever an exception happens (exceptional state).

On the other hand, Return is used to inform the caller that the function executes successfully with whatever output even if nullptr or None.

### 2. Which for Who

**SportsLeagueError:** This is my project umbrella class where it groups any custom user-defined exception
**ValidationError:** When the team name for example is less than 5 characters.
**ConflictError:** Trying to add a new team which is alerady existed.
**NotFoundError:** Trying to access a team/player which is not existed.

### 3. What to log at which level

**DEBUG Level:** This is the development industry, so logs here are limited in use. It is used when developers need to trace an output or check some test cases (testing phase)
**INFO Level:** Only used with basic, routinely procedures.
    - When a new Team/User account created.
    - When User signed in.
**WARNING Level:** When functional/non-functional requirements got violated.
    - User session timeout
    - Failed Login Attempt
    - User 4XX errors
    - Validation errors
**ERROR Level:** When Business Logic drop out, anomalies get to the surface.
    - Server 5XX errors
**CRITICAL Level:** Crashes, Physical Limitations, Unexpected Behaviors
    - Database Collapse
    - Out of Storage errors (disks, servers, etc...)

*note: never include sensitive data like users passwords, PII, system credentials in these logs for security purposes.*

**Scenarios**
A user requests a league that doesn't exist → WARNING Level (404 Not Found error).
The database is completely unreachable → CRITICAL Level (Unexpected Behavior).
An invalid team name was submitted (e.g., 2 characters long) → WARNING Level (Validation error).
The application successfully starts up → INFO Level (Trace the application flow).


### 4. How to handle exceptions in views

This is the time where the developer communicates implicitly with the user. By defining, organizing, maintaining a set of error declarations, examples to follow, guidelines. These techniques help "error avoidance" from the beginning and if an error happened, it informs the user what went wrong and how to handle it afterwards.

This techniques could be:
- Try..Except block
- Decorators

### 5. One anti-pattern

#### Silent Exception Swallowing
This happens when we catch an exception then explicitly do nothing, by forcing the program to continue its flow like this, we drop information along the way making the program actions unreachable, also this could lead to undefined behaviors as this exception should handle such violations happen, so when we 'swallow' the exception, this violation breaks the system. The worst part that we don't know it ever happened and we don't know which exception happened making the maintenance part impossible.

Example:
When the admin try to add a new team (which is existed already but the admin didn't notice it), in normal, this should raise a "ConflictError", but with Silent Exception Swallowing, the new team won't be added and the admin won't know what reason behind this issue.

