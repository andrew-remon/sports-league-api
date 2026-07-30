# third-party
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.db import transaction
from django.db.models import Count

# local
from leagues.models import Team, League, Player, Match, MatchResult
from leagues.services import get_standings
from leagues.filters import TeamFilter, PlayerFilter, MatchFilter
from leagues.serializers import (
    LeagueSerializer,
    MatchSerializer,
    PlayerSerializer,
    MatchResultSerializer,
    StandingsSerializer,
    TeamListSerializer,
    TeamDetailSerializer,
)
from leagues.permissions import IsLeagueOwnerOrReadOnly, IsMatchLeagueOwnerOrReadOnly, IsTeamLeagueOwnerOrReadOnly

# Create your views here.
class LeagueViewSet(ModelViewSet):
    """
    Manage leagues and expose computed standings.

    Standings are not a stored field — they're computed on read
    via `get_standings()` and serialized with StandingsSerializer,
    which is why `get_serializer_class` branches on `self.action`.
    """

    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    permission_classes = [IsLeagueOwnerOrReadOnly]
    ordering_fields = ["name", "created_at"]
    search_fields = ["name"]

    def get_serializer_class(self):
        if self.action == "standings":
            return StandingsSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @extend_schema(
        summary="Create standings table for a specific league.",
        description="Calculates every team record stats,"
        "then serializes each record by StandingsSerializer and creates the standings table.",
        responses={
            200: StandingsSerializer(many=True),
            404: OpenApiResponse(description="League ID not found"),
        },
    )
    @action(detail=True, methods=["get"])
    def standings(self, request, pk=None):
        standings = get_standings(pk)
        serializer = self.get_serializer(standings, many=True)  # many=true returns a ListSerializer
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamViewSet(ModelViewSet):
    """
    Manage Teams and display full list of a specific Team's players.

    `league` filtering is handled declaratively by `TeamFilter`
    (see `filterset_class`), not in `get_queryset`.

    `get_queryset` only applies `select_related("league")` and
    `prefetch_related("players")` — these don't filter rows, they
    optimize the SQL executed for `TeamDetailSerializer`'s nested fields.

    `players` action returns the full player list for a single team,
    serialized with `PlayerSerializer` — this is why
    `get_serializer_class` branches on `self.action`.
    """

    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer
    permission_classes = [IsTeamLeagueOwnerOrReadOnly]
    filterset_class = TeamFilter
    ordering_fields = ["name", "founded_year"]
    search_fields = ["name", "city"]

    def get_queryset(self):
        if self.action == "list":
            return super().get_queryset().annotate(player_count=Count("players"))
        return super().get_queryset().select_related("league").prefetch_related("players")

    def get_serializer_class(self):
        if self.action == "players":
            return PlayerSerializer
        if self.action == "list":
            return TeamListSerializer
        return super().get_serializer_class()

    @extend_schema(
        summary="Show all players of a specific team",
        description="Filters from players table with the specific team ID, then shows each player record",
        responses={
            200: PlayerSerializer(many=True),
            404: OpenApiResponse(description="Team ID not found"),
        },
    )
    @action(detail=True, methods=["get"])
    def players(self, request, pk=None):
        players = Player.objects.filter(team__pk=pk).select_related("team")
        # we use get_serializer method to preserve the context(request, formal, view)
        serializer = self.get_serializer(players, many=True)  # was: PlayerSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlayerViewSet(ModelViewSet):
    """
    Manage Players with filtering, search and ordering.

    'position' and 'team' filtering is handled declaratively by
    `PlayerFilter` (see `filterset_class`), not in `get_queryset`.
    """

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = PlayerFilter
    ordering_fields = ["last_name", "jersey_number"]
    search_fields = ["first_name", "last_name"]

    def get_queryset(self):
        """
        Return players with `team__league` pre-joined via select_related.

        `get_queryset` applies `select_related("team__league")` because
        `PlayerSerializer` traverses two FK levels (player -> team -> league).
        Depth here must match serializer field depth — if the serializer
        starts nesting further, this needs to go deeper too.
        """
        return super().get_queryset().select_related("team")


class MatchViewSet(ModelViewSet):
    """
    Manage matches with filtering, ordering, searching.

    'league' filtering is handled declaratively by `MatchFilter`
    (see `filterset_class`), not in `get_queryset`.

    `record_result` (see `@action`) mutates `match.status` to
    COMPLETED and creates the associated `MatchResult` — this is
    the only state-changing custom action in this ViewSet, if `result` attribute
    found in match instance, a validation error pops up.
    """

    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsMatchLeagueOwnerOrReadOnly]
    filterset_class = MatchFilter
    ordering_fields = ["scheduled_date", "match_day"]
    search_fields = ["home_team__name", "away_team__name"]

    def get_queryset(self):
        """
        Return matches with `result` pre-joined via select_related.

        `MatchSerializer` nests `MatchResult` as a full object, which
        would otherwise trigger one query per row (N+1). `home_team`,
        `away_team`, `league` are serialized as plain FK ids — no JOIN
        needed since that data is already on the `Match` row.
        """
        return super().get_queryset().select_related("result") # reverse OneToOne field - only exception to use with select_related()

    @extend_schema(
        summary="Record Match Score Result",
        description="Submits the final score for a scheduled match."
        "This marks the match status as COMPLETED and creates the associated MatchResult record.",
        request=MatchResultSerializer,
        responses={
            201: MatchResultSerializer,
            400: OpenApiResponse(description="Invalid request payload (e.g, negative scores, invalid match ID)"),
            404: OpenApiResponse(description="Match Not Found"),
        },
    )
    @action(detail=True, methods=["post"])
    def record_result(self, request, pk=None):
        match = self.get_object()

        if MatchResult.objects.filter(match=match).exists():
            return Response(data={"detail": "A result already exists for this match."}, status=status.HTTP_409_CONFLICT)

        serializer = MatchResultSerializer(data=request.data, context=self.get_serializer_context())  # deserialization
        serializer.is_valid(raise_exception=True)
        # first match: refer to the field in MatchResultSerializer,
        # should be the same name, as this will be the kwarg key before saving.
        # second match: the match variable in this method

        with transaction.atomic():
            serializer.save(match=match)
            match.status = Match.MatchStatus.COMPLETED
            match.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)  # serialization
