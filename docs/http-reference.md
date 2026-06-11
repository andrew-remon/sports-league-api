## Methods Table

| Method   |  Safe?   | Idempotent | Has Body? | Sports League API example |
|----------|----------|------------|-----------|---------------------------|
| GET      |   Yes    |   Yes      |    NO     | Retrieve all teams info from Standings|
| PUT      |   NO     |   Yes      |    Yes    | Update Standings before new season begins|
| POST     |   NO     |   NO       |    Yes    | Register a new team to the league at the start of the season|
| PATCH    |   NO     |   NO       |    Yes    | After a match ends, update only the team's points, wins, and goals scored in standings — not the full record|
| HEAD     |   Yes    |   Yes      |    NO     | Retrieve only League Metadata (season #, league name, country)|
| DELETE   |   NO     |   Yes      |    NO     | Delete Player record who moved to another team|
| OPTIONS  |   Yes    |   Yes      |    NO     | When Frontend layer needs to deal with Backend APIs - Browser preflight check before sending a --non-simple-- method the League |

---

## Status codes Table

|   Code   |   Name   |          When to use        | Sports League API example |
|----------|----------|-----------------------------|---------------------------|
|   200    |    OK    |  When the request succeeded | Sports League Standings is shown successfully on the browser|
|   201    |  Created | When the request succeeded and a new resource is created | POST /leagues/ successfully creates a new league — server returns 201 with the newly created league data |
|   204    | No Content | When no content to send for this request | Admin successfully deletes a player record — server confirms deletion but returns no body |
|   301    | Moved Permanently | When the URL of the requested resource has been changed permanently | API endpoint permanently changed from /api/v1/leagues/ to /api/v2/leagues/ — old URL redirects to new one forever |
|   302    |  Found  | This response code means that the URI of requested resource has been changed temporarily | During scheduled maintenance, all requests are temporarily redirected to a maintenance page — original URL will be restored |
|   304    | Not Modified | When the response has not been modified so the client can continue to use the same cached version of the response | Client requests standings — server confirms data hasn't changed since last fetch, client uses its existing cached copy |
|   400    | Bad Request | When the server perceives an error from the client side | POST /leagues/ sent with malformed JSON body or without the required name field |
|   401    | Unauthorized | When the client must authenticate itself to get the requested response | The admin of Sports League must authenticate (login/register) before any action taken |
|   403    | Forbidden | When the client does not have access rights to the content | A logged-in regular user (not an admin) tries to DELETE /leagues/1/ — the server knows who they are but rejects the action |
|   404    | Not Found | When the server cannot find the requested resource | the User tries to access and unidentified page to the server, page that is not found |
|   405    | Method Not Allowed | When the request method is known by the server but is not supported by the target resource | Admin tries try to delete a record while API may not allow DELETE method |
|   409    | Conflict  | When a request conflicts with the current state of the server | the Admin tries to add an existed team to the standings or update X+1 team records while there are only X standings records |
|   413    | Content Too Large | When the request body is larger than limits defined by server | Admin uploads a 50MB team logo image but the server's max allowed upload size is 5MB |
|   415    | Unsupported Media Type | When the media format of the requested data is not supported by the server | Request sent with Content-Type: text/plain but the API only accepts application/json |
|   422    | Unprocessable Content | When the request was well-formed but was unable to be followed due to semantic errors (business logic) | POST /teams/ sent with founded_year: 1800 — JSON is valid, but the value fails business logic validation (year out of acceptable range) |
|   429    | Too Many Requests | When the user has sent too many requests in a given amount of time | A client sends 200 requests to GET /standings/ within 1 minute, exceeding the API's rate limit of 100 requests/minute |
|   500    | Internal Server Error | The server has encountered a situation it does not know how to handle | SAn unhandled exception in the Django view crashes the server while calculating match results |
|   502    | Bad Gateway | When the server, while working as a gateway to get a response needed to handle the request, got an invalid response | Nginx (the proxy) tries to forward a request to the Django app server, but Django is down — Nginx returns 502 to the client |
|   503    | Service Unavailable | When the server is not ready to handle the request (maintenance, older version, overload) | The Sports League database is being migrated — server is temporarily offline and returns 503 until migration completes |
|   504    | Gateway Timeout | when the server is acting as a gateway and cannot get a response in time | A complex league standings query takes 35 seconds — Nginx's 30-second timeout expires before Django responds, returning 504 |

---

## Key headers Table

| Header | Purpose | Example value |
|--------|---------|---------------|
| Host   | Define the domain name server | sports-league-api.com |
| User-Agent | Identify the client | Chrome/143.0.0.0 Mobile Safari/537.36 |
| Authorization | Carry Authentication credentials (client's identity) | Bearer eyJhbGciOiJIUzI1NiJ9...|
| Accept | Define what content client can handle | text/html, application/json |
| Accept-Encoding | Define Compression method client can understand | gzip, br |
| Accept-Language | Preferred language to the client | en-US, en;q=0.9|
| Cookie | Send stored cookie to the server | sessionId=abc123 |
| Content-Type (request) | Define Format of the request body | application/json |
| Content-Length (request) | Define Size of request body | 348 |
| Content-Type (response) | Define Type of returned data | text/html |
| Content-Length (response) | Define Size of response body | 2048 |
| Set-Cookie | Send Cookie to be stored by Client | sessionId=abc123; HttpOnly |
| Cache-Control | Control Caching Behavior | no-cache |
| Date | Define timestamp of Message | Mon, 08 Jun 2026 10:00:00 GMT |

---
---

# Richardson Maturity Model applied to Sports League API

## Level 0: The Swamp of POX (Plain Old XML/JSON)
**Description:** At this level, HTTP is used purely as a transport protocol (tunneling). The API has a single endpoint (a "smart endpoint") and accepts only one HTTP method (typically `POST`). The actual operation and resource details are buried inside the request body. All responses return `200 OK` regardless of success or failure, with error details serialized within the response payload.
* **Endpoint:** `POST /api/sportsleague`
* **Request Example (Get Standings):**
  ```json
  {
    "action": "get_standings",
    "league_id": 42
  }
  ```
* **Request Example (Create Team):**
  ```json
  {
    "action": "create_team",
    "league_id": 42,
    "team_name": "Red Devils"
  }
  ```
* **Real-World Connection:** While academically discouraged for REST, this pattern is the foundation of **SOAP**, **GraphQL** (single `POST /graphql` endpoint), and **gRPC** (tunneling over HTTP/2).

---

## Level 1: Resources
**Description:** This level introduces the concept of **Resources** (individual URIs) instead of routing everything through a single endpoint. We divide the system into distinct business entities (e.g., leagues, teams, players). However, we still tunnel actions through a single HTTP method (typically `POST`).
* **Endpoints:**
  * `POST /api/leagues/42` (To fetch league details)
  * `POST /api/leagues/42/create-team` (To add a team)
  * `POST /api/players/123/delete` (To remove a player)
* **Real-World Connection:** This represents an intermediate step toward modularity but suffers from a lack of standard method semantics. Clients must learn custom action endpoints for every resource.

---

## Level 2: HTTP Verbs & Status Codes
**Description:** At this level, we use standard HTTP methods (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) according to their official specifications (safety and idempotency). We also utilize correct HTTP status codes to communicate outcome states instead of returning `200 OK` for failures.
* **Endpoints & Methods:**
  * `GET /api/leagues/42/` -> Retrieve league details (`200 OK` on success, `404 Not Found` if missing)
  * `POST /api/leagues/42/teams/` -> Create a new team in league 42 (`201 Created` on success, `400 Bad Request` if payload is invalid)
  * `PUT /api/teams/1234/` -> Replace/update team details (`200 OK` or `204 No Content`)
  * `DELETE /api/players/99/` -> Remove player 99 (`204 No Content`)
  * `POST /api/leagues/42/teams/` (with a duplicate team name) -> Returns `409 Conflict`
* **Real-World Connection:** **This is the industry standard for REST APIs.** Level 2 strikes the ideal balance between standard HTTP semantics and developer velocity. It is the target level for the Sports League API.

---

## Level 3: Hypermedia Controls (HATEOAS)
**Description:** The highest level of maturity, introducing **HATEOAS (Hypermedia As The Engine Of Application State)**. The server response not only returns the requested data but also provides links to related actions the client can perform next. The API becomes self-documenting, allowing the client to discover actions dynamically.
* **Request:** `GET /api/players/123/`
* **Response Example:**
  ```json
  {
    "id": 123,
    "first_name": "Lionel",
    "last_name": "Messi",
    "position": "FWD",
    "_links": {
      "self": { "href": "/api/players/123/", "method": "GET" },
      "team": { "href": "/api/teams/10/", "method": "GET" },
      "update_profile": { "href": "/api/players/123/", "method": "PATCH" },
      "transfer_player": { "href": "/api/players/123/transfer/", "method": "POST" },
      "retire_player": { "href": "/api/players/123/", "method": "DELETE" }
    }
  }
  ```
* **Real-World Connection:** While theoretically elegant, Level 3 is rarely used in production. It increases payload size, complicates client implementation (clients must parse links rather than constructing URLs), and struggles to integrate with modern type-safe clients (like TypeScript/OpenAPI). Under market demands, Level 2 combined with OpenAPI (Swagger) documentation is preferred.
