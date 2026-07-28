  ## Comparison between different Authentication schemes

  | Factor | Session Auth | Token (DRF) | JWT |
  |---|---|---|---|
  | Statefulness | Server-side | Server-side | Stateless |
  | Scalability | Need shared store | Need shared DB | No shared state |
  | Revocability | Easy (delete session) | Easy (delete token) | Hard (need blacklist) |
  | CSRF risk | Yes (cookie-based) | No (header-based) | Depends on storage |
  | Best for | Server-rendered apps | Simple APIs | Distributed/mobile APIs |


---

## Authentication decision for Sports League API

As this project is for a third-party client, then I'll use:
* `**JWT**` for API endpoints.
* `**session auth**` for Django admin.

this project is suitable for JWT, here's why:
- No need for frequent stateful validation, as the user just signed in, check his favorite team, league, player, match, etc...
- Fast app: the app doesn't need continual data about the user itself, so instant computation like JWT does with no DB lookups makes it much faster and efficient.
- Secured and Tamper-proof.
- Also session auth is the right call for Django admin, as it consider client-server render and in this situation, a defined session need to be stored to handle different permissions. Number of DB lookups won't bother or affect the process because the number of admins who handles data are no compare with the users who actually use the application daily and intensively.

## Token Storage

Tokens will be stored in header `Authorization: Bearer <token>` not cookie to avoid the CSRF vulnerability and reduce the request body noise. On the other hand, token encoding required a bit of storage which could be challenging with large header payload. and it's vulnerable to XSS (Cross-site scripting) attacks where an attacker could inject one line of JS code into your website script and get your token - one it is exposed to him, impersonation and theft crisis could happen.

---

## Token Lifecycle

1. **Registration / Login:** User submits credentials (`email` and `password`) to `POST /api/v1/auth/login/`.
2. **Token Generation:** The authentication server validates the credentials and returns a JSON payload containing an **Access Token** and a **Refresh Token**.
3. **Storage:** The client (frontend) securely stores both tokens (e.g., in memory or HttpOnly cookies).
4. **Authenticated Requests:** For protected API endpoints, the client includes the Access Token in the HTTP header:
   `Authorization: Bearer <access_token>`
5. **Validation:** The backend verifies the signature and expiration of the Access Token for each request.
6. **Access Token Expiration (30 Minutes):** When the Access Token expires after 30 minutes, the backend returns a `401 Unauthorized` response. The client transparently requests a new Access Token using `POST /api/v1/auth/refresh/` with the Refresh Token.
7. **Refresh Token Expiration (7 Days) & Rotation:**
   - If token rotation is enabled, using the Refresh Token invalidates (blacklists) the old refresh token and issues a new pair.
   - If the Refresh Token expires (after 7 days without activity) or is blacklisted, the user must log in again with credentials.

---

### Decoded JWT Claims (`docs/jwt_payload.png`)

- **`token_type`**: Identifies token purpose (`"access"` or `"refresh"`).
- **`exp`**: Expiration time formatted as a Unix timestamp (in **seconds** since Jan 1, 1970 UTC).
- **`iat`**: Issued-at time as a Unix timestamp (in **seconds** since Epoch).
- **`jti`**: JWT ID — a unique identifier string for this token (used for tracking and blacklisting).
- **`user_id`**: Unique database ID of the authenticated user.

**Custom Claims:**
- **`email`**: Email address of the logged-in user.
- **`first_name`**: First name of the logged-in user.
