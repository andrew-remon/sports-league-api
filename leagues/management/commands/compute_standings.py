# third-party
from django.core.management.base import BaseCommand, CommandError

# local
from leagues.models import League
from leagues.services import get_standings

class Command(BaseCommand):
    help = "Computes and prints the standings table for a specific league."

    def add_arguments(self, parser):
        # This tells Django to expect a league_id argument
        parser.add_argument(
            'league_id',
            type=int,
            help='The database ID of the league'
        )

    def handle(self, *args, **options):
        league_id = options['league_id']

        # 1. Error Handling: Check if league exists
        try:
            league = League.objects.get(pk=league_id)
        except League.DoesNotExist:
            # Raise CommandError to print a clean error to the user
            raise CommandError(f"League with ID {league_id} does not exist.")

        # 2. Get the standings data
        standings = get_standings(league_id)

        if not standings:
            self.stdout.write(self.style.WARNING(f"No completed matches or teams found for '{league.name}'."))
            return

        # 3. Format and Print the Standings Table
        self.stdout.write(self.style.SUCCESS(f"\nStandings for: {league.name}"))
        self.stdout.write("=" * 75)

        # Header Row
        header = f"{'Pos':<4} {'Team':<20} {'P':<4} {'W':<4} {'D':<4} {'L':<4} {'GF':<4} {'GA':<4} {'GD':<4} {'PTS':<4}"
        self.stdout.write(header)
        self.stdout.write("-" * 75)

        # Data Rows
        for pos, team in enumerate(standings, 1):
            row = (
                f"{pos:<4} "
                f"{team['team_name']:<20} "
                f"{team['played']:<4} "
                f"{team['won']:<4} "
                f"{team['drawn']:<4} "
                f"{team['lost']:<4} "
                f"{team['goals_for']:<4} "
                f"{team['goals_against']:<4} "
                f"{team['goal_difference']:<+4} "  # Adds + or - sign automatically
                f"{team['points']:<4}"
            )
            self.stdout.write(row)

        self.stdout.write("=" * 75 + "\n")
