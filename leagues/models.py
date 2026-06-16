from django.db import models

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
