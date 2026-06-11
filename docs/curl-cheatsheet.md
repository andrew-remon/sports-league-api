### curl -v http://localhost:8000/api/health/

I will use this command when I need to debug an HTTP issue — see the exact headers sent and received, the status code, and the full response. Essential when something isn't working as expected. (By using -v)


### curl -X POST http://localhost:8000/api/leagues/ \
### -H "Content-Type: application/json" \
### -d '{"name": "Premier League", "max_teams": 20}'

I will use `POST` to Create a new resource. The -H flag sets the Content-Type so the server knows to parse the body as JSON. The -d flag is the JSON body I'm sending.


### curl -w "%{time_total}\n" -o /dev/null -s http://localhost:8000/example

I will use this command to Measure how long the server takes to respond, without printing the body. Useful for spotting slow endpoints — if this number grows, something in my view or database query is degrading.


### curl -X PATCH http://localhost:8000/api/leagues/1/ \
###  -H "Content-Type: application/json" \
###  -d '{"max_teams": 18}'.

I will use this command whenever I need to partially update a resource

### curl "http://localhost:8000/api/leagues/?ordering=name&max_teams=20"

I will use this commands whenver I need to check queries parameter and ordering in resources.

