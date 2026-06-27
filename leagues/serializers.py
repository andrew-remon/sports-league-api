from rest_framework import serializers
from leagues.models import League, Team, Player, MatchResult, Match

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model= League
        fields = ["name", "description", "max_teams", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

class TeamSerializer(serializers.ModelSerializer):
    league = serializers.PrimaryKeyRelatedField(queryset=League.objects.all())
    player_count = serializers.SerializerMethodField()

    class Meta:
        model= Team
        fields= ["id", "name", "league", "league_detail", "city", "founded_year", "player_count", "created_at"]

    def get_player_count(self, obj):
        return obj.players.count()

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Team Name must be at least 2 characters.")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["league"] = LeagueSerializer(instance.league).data
        return representation

class PlayerSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ["id", "first_name", "last_name", "full_name", "team", "jersey_number", "position", "date_of_birth"]

    def get_full_name(self, obj):
        return f"{obj.first_name}  {obj.last_name}"

    def validate_jersey_number(self, number):
        if number < 1 or number > 99:
            raise serializers.ValidationError("Jersey Number must be between 1 and 99")
        return number

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["team"] = TeamSerializer(instance.team).data
        return representation

class MatchResultSerializer(serializers.ModelSerializer):
    model = MatchResult
    match = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    class Meta:
        fields = ["id", "match", "home_score", "away_score", "recorded_at"]

class MatchSerializer(serializers.ModelSerializer):
    model = Match
    result = MatchResultSerializer(read_only=True)
    league = serializers.PrimaryKeyRelatedField(queryset=League.objects.all())
    home_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    away_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    class Meta:
        fields = ["id", "league", "home_team", "away_team", "match_day", "scheduled_date", "status", "result"]

    def validate(self, attrs):
        if attrs["home_team"] == attrs["away_team"]:
            raise serializers.ValidationError("A team can't play itself.")

        if attrs["home_team"].league != attrs["away_team"].league:
            raise serializers.ValidationError("League must be the same for two teams.")

        return attrs

class StandingsSerializer(serializers.Serializer):
    team_name = serializers.CharField(max_length=100)
    played = serializers.IntegerField()
    won = serializers.IntegerField()
    drawn = serializers.IntegerField()
    lost = serializers.IntegerField()
    goals_for = serializers.IntegerField()
    goals_against = serializers.IntegerField()
    goal_difference = serializers.IntegerField()
    points = serializers.IntegerField()
