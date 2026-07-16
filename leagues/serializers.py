# third-party
from rest_framework import serializers
from django.db import transaction

# local
from leagues.models import League, Team, Player, MatchResult, Match


class LeagueSerializer(serializers.ModelSerializer):
    """Serializes League instances for the public API."""

    class Meta:
        model = League
        fields = ["id", "name", "description", "max_teams", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class TeamListSerializer(serializers.ModelSerializer):
    player_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "city",
            "player_count"
        ]


class PlayerSerializer(serializers.ModelSerializer):
    """
    Serializes Player instances for the public API,
    including a computed full name and nested team (and league) data.

    `get_full_name` combines `first_name` and `last_name`.

    `validate_jersey_number` rejects any number less than 1 or greater than 99.

    `team` accepts a team ID on write (PrimaryKeyRelatedField) but
    `to_representation` overrides output to nest the full TeamDetailSerializer
    representation (which itself nests League), so reads and writes have
    different shapes for this field.]
    """

    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "team",
            "jersey_number",
            "position",
            "date_of_birth",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def validate_jersey_number(self, number):
        if number < 1 or number > 99:
            raise serializers.ValidationError("Jersey Number must be between 1 and 99")
        return number

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["team"] = TeamListSerializer(instance.team, context=self.context).data
        return representation


class TeamDetailSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "league",
            "city",
            "founded_year",
            "created_at",
            "players",
        ]

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Team Name must be at least 2 characters.")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Pass context through so LeagueSerializer has request access if needed later
        representation["league"] = LeagueSerializer(instance.league, context=self.context).data
        return representation


class MatchResultSerializer(serializers.ModelSerializer):
    """
    Serializes Match Result instances for the public API, exposing the
    related Match as a read-only primary key (no nested Match data).
    `match` is set by the view, not accepted from client input — this
    serializer expects to be used against a specific match's endpoint.
    """

    match = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MatchResult
        fields = ["id", "match", "home_score", "away_score", "recorded_at"]


class MatchSerializer(serializers.ModelSerializer):
    """
    Serializes Match instances for the public API. `result` is nested
    and read-only, populated once a result is recorded via the
    MatchViewSet.record_result action. `league`, `home_team`, and
    `away_team` accept IDs on write.

    `validate` checks that `home_team` and `away_team` differ and
    belong to the same league. This serializer currently only
    supports full creation (no PATCH/PUT), so `validate` assumes
    `home_team` and `away_team` are always present in `attrs`.
    """

    result = MatchResultSerializer(required=False, allow_null=True)
    league = serializers.PrimaryKeyRelatedField(queryset=League.objects.all())
    home_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    away_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    class Meta:
        model = Match
        fields = [
            "id",
            "league",
            "home_team",
            "away_team",
            "match_day",
            "scheduled_date",
            "status",
            "result",
        ]
        read_only_fields = ["status"]

    def create(self, validated_data):
        match = None
        result_data = validated_data.pop('result', None)
        if result_data is not None:
            with transaction.atomic():
                validated_data['status'] = Match.MatchStatus.COMPLETED
                match = Match.objects.create(**validated_data)
                MatchResult.objects.create(match=match, **result_data)
        else:
            validated_data['status'] = Match.MatchStatus.SCHEDULED
            match = Match.objects.create(**validated_data)

        return match

    def validate(self, attrs):
        if attrs["home_team"] == attrs["away_team"]:
            raise serializers.ValidationError("A team can't play itself.")

        if attrs["home_team"].league_id != attrs["away_team"].league_id:
            raise serializers.ValidationError("League must be the same for two teams.")

        if attrs["home_team"].league_id != attrs["league"].id:
            raise serializers.ValidationError("Teams must belong to the specified league.")

        return attrs


class StandingsSerializer(serializers.Serializer):
    """
    Serializes computed league standings data. Unlike other serializers
    in this API, this is a plain Serializer (not ModelSerializer) since
    standings are aggregated from Match/MatchResult records rather than
    stored directly on a model — there is no Standings model to bind to.

    Read-only: this serializer is intended for output only and does not
    implement `create()`/`update()`.
    """

    team_name = serializers.CharField(max_length=100)
    played = serializers.IntegerField()
    won = serializers.IntegerField()
    drawn = serializers.IntegerField()
    lost = serializers.IntegerField()
    goals_for = serializers.IntegerField()
    goals_against = serializers.IntegerField()
    goal_difference = serializers.IntegerField()
    points = serializers.IntegerField()
