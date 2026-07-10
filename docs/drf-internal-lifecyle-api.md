# The Request/Response lifecycle in Django/DRF.

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
