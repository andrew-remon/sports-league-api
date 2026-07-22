# stdlib
import time

# third party
from django.core.management.base import BaseCommand
from django.db import connection, reset_queries

# league
from leagues.models import Team, Player, Match
from leagues.services import get_standings


class Command(BaseCommand):
    help = "Runs key database queries, measures timing and query counts, and outputs a report."

    def handle(self, *args, **options):
        # Define queries inside handle() with descriptive names
        queries_to_test = [
            ("Match Filtering", Match.objects.filter(league_id=1, status='completed').order_by('match_day')),
            ("Team Listing", Team.objects.filter(league_id=1).order_by('name')),
            ("Player Filtering", Player.objects.filter(team_id=1)),
            ("Standings Computation", get_standings(league_id=1))
        ]

        self.stdout.write(self.style.MIGRATE_HEADING("=== Performance Audit Report ==="))

        for name, query in queries_to_test:
            reset_queries()

            start = time.perf_counter()
            results = list(query)  # Force evaluation - force ORM to hit DB
            end = time.perf_counter()

            elapsed_ms = (end - start) * 1000
            db_hits = len(connection.queries)
            sql_executed = connection.queries[0]['sql'] # only when DEBUG = True in settings

            self.stdout.write(self.style.SUCCESS(f"\n[+] {name}"))
            self.stdout.write(f"    SQL: {sql_executed}")
            self.stdout.write(f"    DB Hits: {db_hits}")
            self.stdout.write(f"    Execution Time: {elapsed_ms:.3f} ms")
            self.stdout.write(f"    Rows Returned: {len(results)}")
            self.stdout.write("-" * 50)
