import pytest
from utils.exceptions import ValidationError
from django.db import IntegrityError

from tests.factories import LeagueFactory, MatchFactory, TeamFactory, MatchResultFactory


def test_league_str():
    league = LeagueFactory.build(name="Premier League")
    assert str(league) == "Premier League"

def test_match_clean_same_teams():
    team = TeamFactory.build()
    match = MatchFactory.build(
        home_team=team,
        away_team=team,
    )
    with pytest.raises(ValidationError, match="itself"): # means: a ValidationError must be raised, and its message must contain 'itself'.”
        match.clean()

def test_match_clean_different_leagues():
    league1 = LeagueFactory.build()
    league2 = LeagueFactory.build()
    team1 = TeamFactory.build(league=league1)
    team2 = TeamFactory.build(league=league2)
    match = MatchFactory.build(
        home_team=team1,
        away_team=team2,
        league=league1
    )
    with pytest.raises(ValidationError, match="different league"):
        match.clean()

def test_match_clean_valid_match():
    league = LeagueFactory.build()
    team1 = TeamFactory.build(league=league)
    team2 = TeamFactory.build(league=league)
    match = MatchFactory.build(
        home_team=team1,
        away_team=team2,
        league=league
    )
    match.clean()

def test_match_winner_home(): # check correctness from here
    team1 = TeamFactory.build()
    team2 = TeamFactory.build()
    match = MatchFactory.build(
        completed=True,
        home_team=team1,
        away_team=team2,
    )
    result = MatchResultFactory.build(
        match=match,
        home_score=3,
        away_score=1
    )
    assert(match.winner == team1)

def test_match_winner_away():
    team1 = TeamFactory.build()
    team2 = TeamFactory.build()
    match = MatchFactory.build(
        completed=True,
        home_team=team1,
        away_team=team2,
    )
    result = MatchResultFactory.build(
        match=match,
        home_score=2,
        away_score=5
    )
    assert(match.winner == team2)

def test_match_is_draw():
    team1 = TeamFactory.build()
    team2 = TeamFactory.build()
    match = MatchFactory.build(
        completed=True,
        home_team=team1,
        away_team=team2,
    )
    result = MatchResultFactory.build(
        match=match,
        home_score=1,
        away_score=1
    )
    assert(match.is_draw == True)

def test_match_score_display_scheduled():
    team1 = TeamFactory.build()
    team2 = TeamFactory.build()
    match = MatchFactory.build(
        home_team=team1,
        away_team=team2,
    )
    assert(str(match.score_display) == "Not played")

def test_match_score_display_completed():
    team1 = TeamFactory.build()
    team2 = TeamFactory.build()
    match = MatchFactory.build(
        completed=True,
        home_team=team1,
        away_team=team2,
    )
    result = MatchResultFactory.build(
        match=match,
        home_score=1,
        away_score=1
    )
    assert(str(match.score_display) == f"{result.home_score} - {result.away_score}")

@pytest.mark.django_db
def test_unique_team_name_per_league():
    league = LeagueFactory.create()
    team1 = TeamFactory.create(
        name="Man City",
        league = league
    )
    with pytest.raises(IntegrityError):
        team2 = TeamFactory.create(
            name="Man City",
            league = league
        )

@pytest.mark.django_db
def test_same_team_name_different_leagues():
    league1 = LeagueFactory.create()
    league2 = LeagueFactory.create()
    team1 = TeamFactory.create(
        name="Man City",
        league = league1
    )
    team2 = TeamFactory.create(
        name="Man City",
        league = league2
    )
