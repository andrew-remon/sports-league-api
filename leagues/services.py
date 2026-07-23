# third-party
from django.db.models import Count, Sum, F, OuterRef, Subquery, IntegerField, Window
from django.db.models.functions import Coalesce, DenseRank

# local
from leagues.models import Team, Match


def get_standings(league_id):
    teams = Team.objects.filter(league_id=league_id)

    # --- Subqueries for Home Matches ---
    home_matches = Match.objects.filter(home_team=OuterRef("pk"), status=Match.MatchStatus.COMPLETED)

    home_played_sq = home_matches.values("home_team").annotate(c=Count("pk")).values("c")
    home_won_sq = (
        home_matches.filter(result__home_score__gt=F("result__away_score"))
        .values("home_team")
        .annotate(c=Count("pk"))
        .values("c")
    )
    home_drawn_sq = (
        home_matches.filter(result__home_score=F("result__away_score"))
        .values("home_team")
        .annotate(c=Count("pk"))
        .values("c")
    )
    home_gf_sq = home_matches.values("home_team").annotate(s=Sum("result__home_score")).values("s")
    home_ga_sq = home_matches.values("home_team").annotate(s=Sum("result__away_score")).values("s")

    # --- Subqueries for Away Matches ---
    away_matches = Match.objects.filter(away_team=OuterRef("pk"), status=Match.MatchStatus.COMPLETED)

    away_played_sq = away_matches.values("away_team").annotate(c=Count("pk")).values("c")
    away_won_sq = (
        away_matches.filter(result__away_score__gt=F("result__home_score"))
        .values("away_team")
        .annotate(c=Count("pk"))
        .values("c")
    )
    away_drawn_sq = (
        away_matches.filter(result__away_score=F("result__home_score"))
        .values("away_team")
        .annotate(c=Count("pk"))
        .values("c")
    )
    away_gf_sq = away_matches.values("away_team").annotate(s=Sum("result__away_score")).values("s")
    away_ga_sq = away_matches.values("away_team").annotate(s=Sum("result__home_score")).values("s")

    # Step 1: Annotate using Coalesced Subqueries (returns 0 instead of None if no matches played)
    teams = teams.annotate(
        home_played=Coalesce(Subquery(home_played_sq, output_field=IntegerField()), 0),
        away_played=Coalesce(Subquery(away_played_sq, output_field=IntegerField()), 0),
        home_won=Coalesce(Subquery(home_won_sq, output_field=IntegerField()), 0),
        away_won=Coalesce(Subquery(away_won_sq, output_field=IntegerField()), 0),
        home_drawn=Coalesce(Subquery(home_drawn_sq, output_field=IntegerField()), 0),
        away_drawn=Coalesce(Subquery(away_drawn_sq, output_field=IntegerField()), 0),
        home_goals_for=Coalesce(Subquery(home_gf_sq, output_field=IntegerField()), 0),
        away_goals_for=Coalesce(Subquery(away_gf_sq, output_field=IntegerField()), 0),
        home_goals_against=Coalesce(Subquery(home_ga_sq, output_field=IntegerField()), 0),
        away_goals_against=Coalesce(Subquery(away_ga_sq, output_field=IntegerField()), 0),
    )

    # Step 2: Combine the stats
    teams = teams.annotate(
        played=F("home_played") + F("away_played"),
        won=F("home_won") + F("away_won"),
        drawn=F("home_drawn") + F("away_drawn"),
        goals_for=F("home_goals_for") + F("away_goals_for"),
        goals_against=F("home_goals_against") + F("away_goals_against"),
    ).annotate(
        lost=F("played") - F("won") - F("drawn"),
        goal_difference=F("goals_for") - F("goals_against"),
        points=F("won") * 3 + F("drawn"),
    )

    # ! Step 3: Create the dynamic Window Rank
    teams = teams.annotate(
       rank=Window(
            DenseRank(),
            order_by=[
                F("points").desc(),
                F("goal_difference").desc(),
                F("goals_for").desc()
            ]
        )
    )

    # Step 4: return the exact values dict ordered by 'rank'
    return teams.values(
        team_name=F("name"),
        played=F("played"),
        won=F("won"),
        drawn=F("drawn"),
        lost=F("lost"),
        goals_for=F("goals_for"),
        goals_against=F("goals_against"),
        goal_difference=F("goal_difference"),
        points=F("points"),
        rank=F("rank"),
    ).order_by("rank")

    # ? Old Approach: Python-level sorting and computation
    # return teams.order_by("-points", "-goal_difference", "-goals_for").values(
    #     team_name=F("name"),
    #     played=F("played"),
    #     won=F("won"),
    #     drawn=F("drawn"),
    #     lost=F("lost"),
    #     goals_for=F("goals_for"),
    #     goals_against=F("goals_against"),
    #     goal_difference=F("goal_difference"),
    #     points=F("points"),
    # )
