import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from datetime import timedelta
from django.utils import timezone

from accounts.models import CustomUser
from leagues.models import League, Team, Player, Match, MatchResult


class UserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Sequence(lambda n: f"user{n}@gmail.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.django.Password("user-test-1234")


class LeagueFactory(DjangoModelFactory):
    class Meta:
        model = League

    name = factory.Sequence(lambda n: f"League {n}")
    description = factory.Faker("sentence")
    owner = factory.SubFactory(UserFactory)
    max_teams = 20


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Sequence(lambda n: f"Team {n}")
    league = factory.SubFactory(LeagueFactory)
    city = factory.Faker("city")
    founded_year = fuzzy.FuzzyInteger(1970, 2000)


class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = Player

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    team = factory.SubFactory(TeamFactory)
    jersey_number = factory.Sequence(lambda n: n+1) # jersey number starts from 1
    position = fuzzy.FuzzyChoice(Player.Position.values) # Position here refer to TextChoices not the model field (variable 'position')


class MatchResultFactory(DjangoModelFactory):
    class Meta:
        model = MatchResult

    match = factory.SubFactory("tests.factories.MatchFactory")
    home_score = factory.Faker("random_int", min=0, max=5)
    away_score = factory.Faker("random_int", min=0, max=5)


class MatchFactory(DjangoModelFactory):
    class Meta:
        model = Match

    league = factory.SubFactory(LeagueFactory)
    home_team = factory.SubFactory(
        TeamFactory,
        league=factory.SelfAttribute("..league") # make both teams belong to same league
    )
    away_team = factory.SubFactory(
        TeamFactory,
        league=factory.SelfAttribute("..league")
    )
    match_day = 1
    scheduled_date = factory.LazyFunction(lambda: timezone.now() + timedelta(days=7))
    status = Match.MatchStatus.SCHEDULED

    class Params:
        completed = factory.Trait(
            status = Match.MatchStatus.COMPLETED,
            result = factory.RelatedFactory(
                MatchResultFactory,
                factory_related_name="match" # match here refer to the variable of the reversed FK we used in MatchResult Model
            )
        )
