# Data Model V1

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
