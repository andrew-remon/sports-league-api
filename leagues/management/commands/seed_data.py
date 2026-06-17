from django.core.management.base import BaseCommand
from leagues.models import League, Team, Player

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

        self.stdout.write(self.style.SUCCESS("Database Seeding Completed Successfully!"))
