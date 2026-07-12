# third-party
from django.db import models
from django.db.models import Q, F

# local
from utils.exceptions import ValidationError

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    max_teams = models.PositiveIntegerField(default=20)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        related_name="teams",)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "league"],
                name="unique_team_name_in_league")
            ]

    def __str__(self):
        return self.name


class Player(models.Model):
    class Position(models.TextChoices):
        GOALKEEPER = "GK", "Goal Keeper"
        DEFENDER = "DEF", "Defender"
        MIDFIELDER = "MID", "Midfielder"
        FORWARD = "FWD", "Forward"

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="players",)
    jersey_number = models.PositiveIntegerField()
    position = models.CharField(max_length=3, choices=Position.choices)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Match(models.Model):
    class MatchStatus(models.TextChoices):
    #   ^attr        ^value      ^label (admin panel)
    # Python-only   DB value   Display-only -> DB value used in query parameters
        SCHEDULED = "scheduled", "Scheduled"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        POSTPONED = "postponed", "Postponed"

    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="matches",
    )
    home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="home_matches",
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="away_matches",
    )
    match_day = models.PositiveIntegerField()
    scheduled_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=MatchStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~Q(home_team=F("away_team")),
                name= "different_teams_per_match",
            )
        ]

    def __str__(self):
        return f"{self.home_team} VS {self.away_team}"

    def clean(self):
        # a team can't play itself
        if self.home_team == self.away_team:
            raise ValidationError("A team can't play itself, please enter different team")
        if self.home_team.league != self.league or self.away_team.league != self.league:
            raise ValidationError("A team can't play in a different league")

    def save(self,*args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def winner(self) -> "Team | None":
        if self.status != Match.MatchStatus.COMPLETED:
            return None

        if self.result.home_score > self.result.away_score:
            return self.home_team
        elif self.result.home_score < self.result.away_score:
            return self.away_team
        else:
            return None

    @property
    def is_draw(self) -> bool | None:
        if self.status != Match.MatchStatus.COMPLETED:
            return None
        return self.result.home_score == self.result.away_score

    @property
    def score_display(self) -> str:
        if self.status != Match.MatchStatus.COMPLETED:
            return "Not played"

        return f"{self.result.home_score} - {self.result.away_score}"


class MatchResult(models.Model):
    match = models.OneToOneField(
        Match,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="result",
    )
    home_score = models.PositiveIntegerField()
    away_score = models.PositiveIntegerField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    # no use here since this Model class is inline
    # def __str__(self):
    #     return f"{self.home_score} - {self.away_score}"
