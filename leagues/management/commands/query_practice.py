# third-party
from django.core.management.base import BaseCommand

# local
from django.db.models import Count
from leagues.models import Team, Player


class Command(BaseCommand):
    help = "practice QuerySets examples."

    def handle(self, *args, **options):
        specificTeam = "Real Madrid"
        queries = [
            Team.objects.filter(league__name="Premier League"),
            Player.objects.filter(position=Player.Position.FORWARD),
            Team.objects.annotate(player_count=Count('players')).filter(player_count__gt=0),
            Player.objects.filter(team__name=specificTeam),
        ]
        for queryset in queries:
            self.stdout.write(str(queryset))
            self.stdout.write(str(queryset.query))
            self.stdout.write("--------------------------")

