# third-party
from django.core.management.base import BaseCommand

# local
from leagues.models import League, Match, Team, Player, MatchResult

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

        newcastle, _ = Team.objects.get_or_create(
            name="Newcastle United",
            league=premier_league,
            defaults={
                "city": "Newcastle",
            }
        )

        fulham, _ = Team.objects.get_or_create(
            name="Fulham",
            league=premier_league,
            defaults={
                "city": "London",
            }
        )

        aston_villa, _ = Team.objects.get_or_create(
            name="Aston Villa",
            league=premier_league,
            defaults={
                "city": "Birmingham",
            }
        )

        tottenham, _ = Team.objects.get_or_create(
            name="Tottenham",
            league=premier_league,
            defaults={
                "city": "London",
            }
        )

        bournemouth, _ = Team.objects.get_or_create(
            name="Bournemouth",
            league=premier_league,
            defaults={
                "city": "Bournemouth",
            }
        )

        brentford, _ = Team.objects.get_or_create(
            name="Brentford",
            league=premier_league,
            defaults={
                "city": "London",
            }
        )

        everton, _ = Team.objects.get_or_create(
            name="Everton",
            league=premier_league,
            defaults={
                "city": "Merseyside",
            }
        )

        leeds_united, _ = Team.objects.get_or_create(
            name="Leeds United",
            league=premier_league,
            defaults={
                "city": "Leeds",
            }
        )

        crystal_palace, _ = Team.objects.get_or_create(
            name="Crystal Palace",
            league=premier_league,
            defaults={
                "city": "London",
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

                # === 10 COMPLETED MATCHES ===

        m5, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team=newcastle,
            away_team=fulham,
            status=Match.MatchStatus.COMPLETED,
            defaults={
                "match_day": 1,
            }
        )

        m6, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team=aston_villa,
            away_team=tottenham,
            status=Match.MatchStatus.COMPLETED,
            defaults={
                "match_day": 1,
            }
        )

        m7, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team=bournemouth,
            away_team=brentford,
            status=Match.MatchStatus.COMPLETED,
            defaults={
                "match_day": 2,
            }
        )

        m8, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team=everton,
            away_team=leeds_united,
            status=Match.MatchStatus.COMPLETED,
            defaults={
                "match_day": 2,
            }
        )

        m9, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team=crystal_palace,
            away_team=man_city,
            status=Match.MatchStatus.COMPLETED,
            defaults={
                "match_day": 3,
            }
        )

        m10, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team=liverpool,
            away_team=arsenal,
            status=Match.MatchStatus.COMPLETED,
            defaults={
                "match_day": 3,
            }
        )

        m11, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team=chelsea,
            away_team=newcastle,
            status=Match.MatchStatus.COMPLETED,
            defaults={
                "match_day": 4,
            }
        )

        m12, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team=fulham,
            away_team=aston_villa,
            status=Match.MatchStatus.COMPLETED,
            defaults={
                "match_day": 4,
            }
        )

        m13, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team=tottenham,
            away_team=bournemouth,
            status=Match.MatchStatus.COMPLETED,
            defaults={
                "match_day": 5,
            }
        )

        m14, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team=brentford,
            away_team=everton,
            status=Match.MatchStatus.COMPLETED,
            defaults={
                "match_day": 5,
            }
        )


        # === 5 SCHEDULED MATCHES ===

        m15, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team=leeds_united,
            away_team=crystal_palace,
            status=Match.MatchStatus.SCHEDULED,
            defaults={
                "match_day": 6,
            }
        )

        m16, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team=man_city,
            away_team=arsenal,
            status=Match.MatchStatus.SCHEDULED,
            defaults={
                "match_day": 6,
            }
        )

        m17, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team=liverpool,
            away_team=chelsea,
            status=Match.MatchStatus.SCHEDULED,
            defaults={
                "match_day": 7,
            }
        )

        m18, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team=newcastle,
            away_team=tottenham,
            status=Match.MatchStatus.SCHEDULED,
            defaults={
                "match_day": 7,
            }
        )

        m19, _ = Match.objects.get_or_create(
            league=premier_league,
            home_team=aston_villa,
            away_team=brentford,
            status=Match.MatchStatus.SCHEDULED,
            defaults={
                "match_day": 8,
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

        r3, _ = MatchResult.objects.get_or_create(
            match=m5,
            home_score=2,
            away_score=1,
        )

        r4, _ = MatchResult.objects.get_or_create(
            match=m6,
            home_score=0,
            away_score=2,
        )

        r5, _ = MatchResult.objects.get_or_create(
            match=m7,
            home_score=1,
            away_score=3,
        )

        r6, _ = MatchResult.objects.get_or_create(
            match=m8,
            home_score=2,
            away_score=2,
        )

        r7, _ = MatchResult.objects.get_or_create(
            match=m9,
            home_score=1,
            away_score=0,
        )

        r8, _ = MatchResult.objects.get_or_create(
            match=m10,
            home_score=1,
            away_score=1,
        )

        r9, _ = MatchResult.objects.get_or_create(
            match=m11,
            home_score=3,
            away_score=2,
        )

        r10, _ = MatchResult.objects.get_or_create(
            match=m12,
            home_score=0,
            away_score=0,
        )

        r11, _ = MatchResult.objects.get_or_create(
            match=m13,
            home_score=2,
            away_score=0,
        )

        r12, _ = MatchResult.objects.get_or_create(
            match=m14,
            home_score=1,
            away_score=4,
        )

        self.stdout.write(self.style.SUCCESS("Database Seeding Completed Successfully!"))
