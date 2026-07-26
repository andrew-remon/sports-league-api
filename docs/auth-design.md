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
