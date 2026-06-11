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

