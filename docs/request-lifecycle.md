# What happens when you hit an API endpoint.

### Trace a request to GET https://api.sportsleague.com/leagues/42/

#### My Answer (Refined by Antigravity)

1. User type on the search bar in a web browser: https://api.sportsleague.com/leagues/42/
2. A DNS Recursive Resolver receives the User's request (Port 53). → Application Layer
3. DNS Recursive Resolver queries the root server (.) → Application Layer
4. The resolver queries to root server about TLD Server (.com) → Application Layer
5. root server responds back with the matching TLD server. → Application Layer
6. The resolver sends a request to TLD server asking about the Authoritative (NS) Server.(api.sportsleague) → Application Layer
7. Final Authoritative Server responds with the actual IP Address of the request. → Application Layer
8. IP Packets must be routed through Internet until it reaches the Browser. → Internet Layer
9. Browser & Server initiate a three-way TCP Handshake to establish a stateful connection. → Transport Layer
10. Browser & Server initiate a four-way TLS Handshake to establish secure way of communication (Port 443). → Application Layer
11. Brower make a GET Request:
    GET league/42 http/2
    Host: api.sportsleague.com
    Accept: json/application
    User-agent: Mozilla...
12. Server processes the request (method: GET, protocol: https, target service: /leagues/42). → Application Layer
    Django Processing Step-by-step:
    12.1. Django receives the request throught WSGI/ASGI.
    12.2. Django's urlconf matches /leagues/42 to a view.
    12.3. The view queries the Database.
    12.4. The view serializes the result (DB records) to JSON.
    12.4. Django constructs the HTTP response.
13. The server sends an HTTP response with status 200 OK, ContentType: application/json header, and a JSON body containing the league data for ID 42 → Application Layer
14. JSON Response get rendered on the Browser. → Application Layer
15. After all actions, User closes the website, Browser informs the Server to close Communication. → Transport Layer
16. TCP Communication is closed.

---

#### Antigravity Review

**Phase 1: DNS Resolution (Application Layer)**
1. The user types `https://api.sportsleague.com/leagues/42/` and presses Enter.
The browser first checks its **local DNS cache** (and the OS cache) for a cached A record for `api.sportsleague.com`. If found (and TTL not expired), it skips to Step 6. On a cache miss, it proceeds.
2. The browser sends a DNS query to the configured **Recursive Resolver** (e.g., 8.8.8.8 — Google's public DNS) on **UDP port 53**. → Application Layer
3. The Recursive Resolver, if it doesn't have a cached answer, queries a **Root Name Server (.)** asking: "Who handles .com?" → Application Layer
4. The Root Name Server responds with the address of the **TLD Name Server for .com**. → Application Layer
5. The Recursive Resolver queries the **TLD Name Server (.com)** asking: "Who is the Authoritative Name Server for sportsleague.com?" → Application Layer
6. The TLD Name Server responds with the **Authoritative Name Server (NS)** for `sportsleague.com`. → Application Layer
7. The Recursive Resolver queries the **Authoritative Name Server** for `sportsleague.com` asking: "What is the IP address of `api.sportsleague.com`?" The Authoritative Server responds with an **A record**: e.g., `IP: 93.184.216.34`. DNS resolution is now complete. The path `/leagues/42/` was never involved in DNS. → Application Layer

**Phase 2: TCP Connection (Transport Layer + Internet Layer)**
8. The browser initiates a **TCP 3-way handshake** with `93.184.216.34` on **port 443** (HTTPS uses port 443 by convention; port 80 is plain HTTP).
- Browser → Server: SYN
- Server → Browser: SYN-ACK
- Browser → Server: ACK
A reliable, ordered connection is now established. → Transport Layer (TCP) / Internet Layer (IP routing)

**Phase 3: TLS Handshake (Application Layer)**
9. Over the established TCP connection, the browser and server perform a **TLS handshake** to establish an encrypted channel:
    - Browser sends supported TLS versions and cipher suites (ClientHello)
    - Server responds with its SSL certificate signed by a trusted CA (ServerHello)
    - Browser verifies the certificate (is it signed by a trusted CA? Is it for `api.sportsleague.com`? Has it expired?)
    - Both parties derive a shared session key
    - All subsequent communication is encrypted → Application Layer (TLS)

**Phase 4: HTTP Request (Application Layer)**
10. The browser sends an HTTP GET request over the encrypted TLS channel → Application Layer (HTTP):
    ```
    GET /leagues/42/ HTTP/1.1
    Host: api.sportsleague.com
    Accept: application/json
    User-Agent: Mozilla/5.0 ...
    ```

**Phase 5: Server Processing**
11. The web server (e.g., Nginx) receives the request and forwards it to Django via WSGI/ASGI. → Application Layer
    Django's URL router matches `/leagues/42/` to the`LeagueDetailView`.
    The view calls the ORM: `League.objects.get(id=42)`.
    The ORM generates SQL, PostgreSQL executes it and returns the row.
    The view serializes it to JSON and constructs an HTTP response.

**Phase 6: HTTP Response (Application Layer)** → Application Layer (HTTP)
12. The server sends back:
    ```
    HTTP/1.1 200 OK
    Content-Type: application/json
    Content-Length: 247
    {"id": 42, "name": "Premier League", ...}
    ```
13. The browser receives the response, parses the JSON, and renders the data. → Application Layer

**Phase 7: Connection Close (Transport Layer)**
14. After the response is complete, the TCP connection is closed with a 4-way FIN handshake (or kept alive via `Connection: keep-alive` for subsequent requests). → Transport Layer
