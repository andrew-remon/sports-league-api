# third-party
from django.core.management.base import BaseCommand, CommandError

# local
from leagues.models import League, Match
from leagues.services import get_standings


class Command(BaseCommand):
    help = "Computes and prints the league info, current standing table and the upcoming matches."

    def add_arguments(self, parser):
        parser.add_argument("league_name", type=str, help="The League Name")

    def get_league(self, league_name):
        try:
            league = League.objects.get(name=league_name)
        except League.DoesNotExist:
            raise CommandError(f"League with name {league_name} does not exist.")
        return league

    def print_league_info(self, league):
        teams_count = league.teams.count()
        matches_count = league.matches.count()

        self.stdout.write(f"{'Name:':<4} {league.name}")
        self.stdout.write(f"{'Teams Count:':<4} {teams_count}")
        self.stdout.write(f"{'Matches Count:':<4} {matches_count}")

        self.stdout.write("-" * 60)

    def get_upcoming_matches(self, league):
        upcoming_matches = league.matches.filter(status=Match.MatchStatus.SCHEDULED)

        # Header Row
        header = f"{'Pos':<4} {'Home Team':<20} {'Away Team':<20} {'Date':<10}"
        self.stdout.write(header)
        self.stdout.write("-" * 60)

        # Data Rows
        for pos, match in enumerate(upcoming_matches, 1):
            row = (
                f"{pos:<4} "
                f"{str(match.home_team):<20} "
                f"{str(match.away_team):<20} "
                f"{str(match.scheduled_date):<10} "
            )
            self.stdout.write(row)

        self.stdout.write("=" * 60 + "\n")

    def handle(self, *args, **options):
        league = self.get_league(options["league_name"])
        self.print_league_info(league)
        get_standings(league.id)
        self.get_upcoming_matches(league)
