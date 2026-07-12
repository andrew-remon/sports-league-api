# third-party
from django_filters import rest_framework as filters

# local
from leagues.models import Team, Player, Match

class TeamFilter(filters.FilterSet):
    class Meta:
        model = Team
        fields = ['league', 'city']

class PlayerFilter(filters.FilterSet):
    league = filters.NumberFilter(field_name="team__league")

    class Meta:
        model = Player
        fields = ['team', 'position', 'league']

class MatchFilter(filters.FilterSet):
    scheduled_date = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Match
        fields = ['league', 'status', 'match_day', 'scheduled_date']
