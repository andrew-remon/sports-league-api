# A step-by-step diagram of the Django request/response lifecycle

## 1. Middleware Stack

*note:* it goes from top to bottom in request phase, bottom to top in response phase.

Security Middleware
        ↓
Session Middleware
        ↓
Common Middleware
        ↓
CSRFView Middleware
        ↓
Authentication Middleware
        ↓
LoginRequired Middleware (optional)
        ↓
Message Middleware
        ↓
XFrameOptionsMiddleware

---

## 2. Where URL resolution happens

- After the user requests a URL, Django determines the URLconf module to use (whether ROOt_URLCONF or a specified one from the request itself), Django installs the module, looks for urlpatterns variable, match every URL found there with the requested one till it found a matched URL or an error handling view.

---

## 3. Where the view function executes

- After URL get resoluted and identified, the path instance has an argument with the suitable view function (or class-based view) to this URL, so mapping is happening between the matched URL and the view function. view get a request, process it, then give a response.

---

## 4. Where exceptions are caught

- Exceptions are caught throughout the whole lifecycle:
    - when No URL matched found.
    - in Middleware different headers (using process_exception method)
    - request/response processing in views

---

## 5. For each middleware, include one sentence about what it does

- Security Middleware: enforces HTTPS by redirecting HTTP requests to HTTPS using `SECURE_SSL_REDIRECT = True` and other headers.
- Session Middleware: it's a bridge between HTTP cookie and request.session (read from request, update from response if changed)
- Common Middleware: checks that all URLs have one common pattern (using techniques like APPEND_SLASH, etc...)
- CSRFView Middlware: validates that the CSRF token in the request matches the token in the cookie, on every unsafe HTTP method.
- Authenticate Middleware: resolves who the requester (from Session Middleware) is and attaches them to `request.user`
- LoginRequired Middleware: enforces that every request have a real user after AuthenticateMiddleware inspects from the session and its cookie Anonymous
- Message Middleware: handles one-time messages anywhere in Django
- XFrameOptionsMiddleware: prevents clickjacking attacks by setting the X-Frame-Options header on responses.

---

## 6. Mark the point where request.user becomes available

request.user becomes available after AuthenticateMiddleware process done, AuthenticateMiddleware reads data from sessions and their cookies (provided by Session Middleware) then assigns this data to request.user.
