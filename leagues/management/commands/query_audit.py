# third party
from django.db import connection, reset_queries
from django.test import Client
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Calls each API endpoint programmatically (using Django's test client) and counts the queries"

    ENDPOINTS = [
        # League
        ("GET", "/api/v1/leagues/"),
        ("GET", "/api/v1/leagues/1/"),
        ("GET", "/api/v1/leagues/1/standings/"),   # ← custom action, was missing

        # Team
        ("GET", "/api/v1/teams/"),
        ("GET", "/api/v1/teams/1/"),
        ("GET", "/api/v1/teams/14/players/"),      # ← custom action, was missing

        # Player
        ("GET", "/api/v1/players/"),
        ("GET", "/api/v1/players/3/"),

        # Match
        ("GET", "/api/v1/matches/"),
        ("GET", "/api/v1/matches/6/"),
        # record_result is POST — skip it in the audit (it mutates data)
    ]

    def handle(self, *args, **options):
        client = Client()

        for endpoint in self.ENDPOINTS:
            reset_queries()
            method, path = endpoint # unpack it first
            client.get(path, SERVER_NAME = "localhost")
            queries = connection.queries
            print(path) 
            print(len(queries))
            for query in queries:
                print(query["sql"][:120]) # cut the query to the first 120 chars
            print("---------------------------------------")

