from rest_framework import serializers
from leagues.models import League

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model= League
        fields = ["name", "description", "max_teams", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

