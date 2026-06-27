# Data Model V1

## Model Relations
### League | Team
**relation:** 1:N
**on_delete:** CASCADE
    *(No team can be existed without be linked to a specific league)*
**related_name:** teams


### Team | Player
**relation:** 1:N
**on_delete:** SET_NULL
    *(any player could be registered without yet assigned to a team (hence set null))*
**related_name:** players

---

## API Design Decisions V1

1. URL Structure: /api/v1
2. Pagination Strategy: 20 per page
3. Error Response Format (Django Default Format):
    - Flat field → {"field": ["error"]}
    - Nested serializer field → {"field": {"subfield": ["error"]}}
4. In errors field: Converting {"detail": "..."} into {"field": null, "message": "..."} → the custom exception handler will have only one way to iterate over errors field not matter the error type(Auth, Validation, etc...).
