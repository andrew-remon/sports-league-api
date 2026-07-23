## Views

#### get_queryset() method (ViewSet)
→ it's the **data scope** that ModelMixins (list/retrieve) call and deal with internally.
→ It happens before the serialization phase.
→ It is responsible for query optimization (fast access, avoiding N+1 issue, etc...)

#### @action decorator
→ is a decorator that tells the router to generate an extra URL for a method that isn't one of the six default CRUD operations (list, create, retrieve, update, partial_update, destroy).

---

## Serializers

→ Is designed by default to serialize one object at a time.
→ Using `many=true` implies that this data is iterable/a collection. so to_representation() method inside BaseSerializer runs once per item.
→ In the project: PlayerSerializer.to_representation() → calls TeamDetailSerializer(instance.team).data → which itself calls LeagueSerializer(instance.league).data.
→ any field whose value is derived from the URL, request.user, or view logic — not from the request body — should be read_only=True on the serializer.

→ DRF Serializer Internals
```text
is_valid()
 └─ run_validation(initial_data)
      └─ to_internal_value(data)                     # serializer-level orchestrator
           for each field:
             ├─ field.run_validation(raw_value)       # FIELD-LEVEL
             │    ├─ validate_empty_values()
             │    ├─ field.to_internal_value()
             │    └─ field.validators (run_validators)
             └─ validate_<field_name>(value)           # SERIALIZER-LEVEL, per-field
      └─ run_validators(value)                         # serializer.validators (class Meta level, rare)
      └─ self.validate(attrs)                          # OBJECT-LEVEL, cross-field
 └─ self._validated_data = attrs   (if no errors raised anywhere above)
```

---

## URLs

#### reverse() method → when basename=None in urls router
league-list       → GET/POST /leagues/
league-detail     → GET/PUT/PATCH/DELETE /leagues/{pk}/
league-standings  → GET /leagues/{pk}/standings/   (from your @action)

team-list         → GET/POST /teams/
team-detail       → GET/PUT/PATCH/DELETE /teams/{pk}/
team-players      → GET /teams/{pk}/players/   (from your @action)

If you need *multiple independent search params* — e.g. searching team name and player name separately in the same request, then in get_queryset() method, we define **self.request.query_params.get()**, otherwise use **Search Filter**


---

## Intersections

#### select_related() method
Although it's defined in get_queryset() method in ViewSet, but it's coupled with its serializer because serializer shapes data based on the fields given row by row, if the field was an internal one from a foreign table, a N+1 issue occurs.
That's why in this method **we define all fields that will be used by the serializer and isn't directly in the table** (foreign keys, one to one relationship)

#### checklist points
1. Does the field use PrimaryKeyRelatedField? → no join needed, field_id is free.
2. Does the field use a nested serializer or source='related.attr'? → join needed for that hop.
3. Does to_representation() call another serializer? → follow that chain, join needs to cover every hop.
4. Does a SerializerMethodField call .count()? → prefetch is useless, .count() always hits DB fresh. Use len(obj.related.all()) if you want the prefetch cache respected.
5. Match select_related/prefetch_related depth to the deepest traversal found in steps 2–4, not to every FK the model happens to have.


#### The request/response lifecycle skeleton

```text
1. WSGI/ASGI server (runserver / gunicorn) receives raw HTTP
2. Django's WSGIHandler.__call__() → builds HttpRequest
3. Middleware stack (request phase, top→bottom in MIDDLEWARE list)
4. URL resolver (urls.py) → matches path to a view
5. DRF APIView.dispatch() ← THIS is where DRF takes over from Django
   ├─ self.initial(request) → runs authentication, permissions, throttling
   ├─ handler = getattr(self, request.method.lower())  # e.g. self.post
   └─ response = handler(request, *args, **kwargs)
6. Inside your ViewSet method (e.g. create() from CreateModelMixin):
   ├─ serializer = self.get_serializer(data=request.data)
   ├─ serializer.is_valid(raise_exception=True)
   │    └─ runs validate_<field>() → validate() → collects errors
   ├─ self.perform_create(serializer)
   │    └─ serializer.save() → calls serializer.create()
   └─ return Response(serializer.data, status=201)
7. Middleware stack (response phase, bottom→top)
8. WSGIHandler converts HttpResponse back to raw HTTP
```

```text
1. URL resolves → router maps it to ViewSet class
2. New instance created, request attached
3. dispatch() runs on that instance
4. dispatch() determines HTTP verb → looks up mapped method name (e.g. "create")
5. dispatch() CALLS that method (e.g. self.create(request))
   → this call IS the mixin executing — not a separate later step
6. INSIDE that method, serialization happens:
   - get_serializer(data=request.data)
   - is_valid()
   - save()
7. Method returns a Response object
8. dispatch() returns that Response
```
