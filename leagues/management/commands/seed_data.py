from django.core.management.base import BaseCommand
from leagues.models import *

class Command(BaseCommand):
    help = "seeds the database with inital leagues, teams and players."

    def handle(self, *args, **options):
        self.stdout.write("Starting Database Seeding...")

        # ----------------- Leagues Creation ---------------------
        premier_league, _ = League.objects.get_or_create(
            name="Premier League",
            defaults={
                "max_teams": 20,
            })

        la_liga, _ = League.objects.get_or_create(
            name="La Liga",
            defaults= {
                "max_teams":20,
            }
        )

        bundesliga, _ = League.objects.get_or_create(
            name="Bundesliga",
            defaults= {
                "max_teams": 20,
            }
        )

        # ----------------- Teams Creation ---------------------
        real_madrid, _ = Team.objects.get_or_create(
            name= "Real Madrid",
            league= la_liga,
            defaults= {
                "city":"Madrid",
            }
        )

        barcelona, _ = Team.objects.get_or_create(
            name= "Barcelona",
            league= la_liga,
            defaults= {
                "city":"Barcelona",
            }
        )

        man_city, _ = Team.objects.get_or_create(
            name= "Manchester City",
            league= premier_league,
            defaults= {
                "city":"Manchester",
            }
        )

        liverpool, _ = Team.objects.get_or_create(
            name= "Liverpool",
            league= premier_league,
            defaults= {
                "city":"Merseyside",
            }
        )

        arsenal, _ = Team.objects.get_or_create(
            name="Arsenal",
            league=premier_league,
            defaults= {
                "city":"London",
            }
        )

        bayern_munich, _ = Team.objects.get_or_create(
            name="Bayern Munich",
            league=bundesliga,
            defaults={
                "city":"Munich",
            }
        )

        borussia_dortmund, _ = Team.objects.get_or_create(
            name="Borussia Dortmund",
            league=bundesliga,
            defaults= {
                "city":"Dortmund",
            }
        )

        leipzig, _ = Team.objects.get_or_create(
            name="Leipzig",
            league=bundesliga,
            defaults={
                "city":"Leipzig",
            }
        )

        chelsea, _ = Team.objects.get_or_create(
            name="Chelsea",
            league=premier_league,
            defaults= {
                "city":"London",
            }
        )

        # ----------------- Players Creation ---------------------
        p1 = Player.objects.get_or_create(
            first_name="Kylian",
            last_name="Mbappe",
            team= real_madrid,
            defaults={
                "jersey_number":10,
                "position":Player.Position.FORWARD,
            }
        )

        p2 = Player.objects.get_or_create(
            first_name="Jude",
            last_name="Bellingham",
            team= real_madrid,
            defaults={
                "jersey_number":5,
                "position":Player.Position.MIDFIELDER,
            }
        )

        p3 = Player.objects.get_or_create(
            first_name="Pedri",
            last_name="Gonzalez",
            team= barcelona,
            defaults={
                "jersey_number":8,
                "position":Player.Position.MIDFIELDER,
            }
        )

        p4 = Player.objects.get_or_create(
            first_name="Lamine",
            last_name="Yamal",
            team= barcelona,
            defaults={
                "jersey_number":10,
                "position":Player.Position.FORWARD,
            }
        )

        p5 = Player.objects.get_or_create(
            first_name="Erling",
            last_name="Halaand",
            team= man_city,
            defaults={
                "jersey_number":9,
                "position":Player.Position.FORWARD,
            }
        )

        p6 = Player.objects.get_or_create(
            first_name="Marc",
            last_name="Guehi",
            team= man_city,
            defaults={
                "jersey_number":15,
                "position":Player.Position.DEFENDER,
            }
        )

        p7 = Player.objects.get_or_create(
            first_name="Virgil",
            last_name="Van Dijk",
            team= liverpool,
            defaults={
                "jersey_number":4,
                "position":Player.Position.DEFENDER,
            }
        )

        p8 = Player.objects.get_or_create(
            first_name="Allison",
            last_name="Beker",
            team= liverpool,
            defaults={
                "jersey_number":1,
                "position":Player.Position.GOALKEEPER,
            }
        )

        p9 = Player.objects.get_or_create(
            first_name= "Eder",
            last_name= "Militao",
            team= real_madrid,
            defaults= {
                "jersey_number": 3,
                "position": Player.Position.DEFENDER,
            }
        )

        p10 = Player.objects.get_or_create(
            first_name= "William",
            last_name= "Saliba",
            team=arsenal,
            defaults= {
                "jersey_number": 2,
                "position": Player.Position.DEFENDER,
            }
        )

        p11 = Player.objects.get_or_create(
            first_name= "Declan",
            last_name= "Rice",
            team= arsenal,
            defaults= {
                "jersey_number": 41,
                "position": Player.Position.MIDFIELDER,
            }
        )

        p12 = Player.objects.get_or_create(
            first_name= "Leandro",
            last_name= "Trossard",
            team= arsenal,
            defaults= {
                "jersey_number": 19,
                "position": Player.Position.FORWARD,
            }
        )

        p13 = Player.objects.get_or_create(
            first_name= "Manuel",
            last_name= "Neuer",
            team= bayern_munich,
            defaults= {
                "jersey_number": 1,
                "position": Player.Position.GOALKEEPER,
            }
        )

        p14 = Player.objects.get_or_create(
            first_name= "Harry",
            last_name= "Kane",
            team=bayern_munich,
            defaults= {
                "jersey_number": 9,
                "position": Player.Position.FORWARD,
            }
        )

        p15 = Player.objects.get_or_create(
            first_name= "Luis",
            last_name= "Diaz",
            team=bayern_munich,
            defaults= {
                "jersey_number": 14,
                "position": Player.Position.FORWARD,
            }
        )

        p16 = Player.objects.get_or_create(
            first_name= "Yan",
            last_name= "Couto",
            team= borussia_dortmund,
            defaults= {
                "jersey_number": 2,
                "position": Player.Position.DEFENDER,
            }
        )

        p17 = Player.objects.get_or_create(
            first_name= "Ramy",
            last_name= "Bensebaini",
            team= borussia_dortmund,
            defaults= {
                "jersey_number": 5,
                "position": Player.Position.DEFENDER,
            }
        )

        p18 = Player.objects.get_or_create(
            first_name= "Felix",
            last_name= "Nmecha",
            team= borussia_dortmund,
            defaults= {
                "jersey_number": 8,
                "position": Player.Position.MIDFIELDER,
            }
        )

        # ----------------- Matches Creation ---------------------

        m1, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team = man_city,
            away_team=liverpool,
            status = Match.MatchStatus.COMPLETED,
            defaults={
                "match_day": 5,
            }
        )

        m2, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team = arsenal,
            away_team=chelsea,
            status = Match.MatchStatus.SCHEDULED,
            defaults={
                "match_day": 7,
            }
        )

        m3, _ = Match.objects.get_or_create(
            league=la_liga,
            home_team = real_madrid,
            away_team=barcelona,
            status = Match.MatchStatus.COMPLETED,
            defaults={
                "match_day": 2,
            }
        )

        m4, _ = Match.objects.get_or_create(
            league=bundesliga,
            home_team = bayern_munich,
            away_team=borussia_dortmund,
            status = Match.MatchStatus.SCHEDULED,
            defaults={
                "match_day": 11,
            }
        )

        # ----------------- Matches Result Creation ---------------------
        r1, _ = MatchResult.objects.get_or_create(
            match=m1,
            home_score=3,
            away_score=0,
        )

        r2, _ = MatchResult.objects.get_or_create(
            match=m3,
            home_score=4,
            away_score=2,
        )

        self.stdout.write(self.style.SUCCESS("Database Seeding Completed Successfully!"))
