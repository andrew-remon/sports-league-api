from django.contrib import admin
from django.db.models import Count
from .models import *

# Register your models here.
@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', "max_teams", 'created_at', 'get_team_count')
    search_fields = ('name',)

    # these two methods represent Separation of Concerns: Fetching and Displaying

    # this method is used to fetch the data from Database
    def get_queryset(self, request):
        queryset = super().get_queryset(request) # to override the base function
        return queryset.annotate(teams_count=Count('teams'))

    # this method get the value of ORM method above and display it (UI)
    @admin.display(description='Teams Registered', ordering='teams_count')
    def get_team_count(self, obj):
        return obj.teams_count


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'city')
    list_select_related = ('league',)
    list_filter = ('league',)
    search_fields = ('name', 'city', )


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'team', 'position', 'jersey_number')
    list_select_related = ('team',)
    list_filter = ('position', 'team')
    search_fields = ('first_name', 'last_name', 'jersey_number')

    @admin.display(description='Full Name', ordering='first_name')
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MatchResultInline(admin.TabularInline):
    model = MatchResult
    extra = 0


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    inlines = [MatchResultInline]
    list_display = ('league', 'home_team', 'away_team', 'status', 'scheduled_date', 'get_match_result')

    @admin.display(description="Match Result")
    def get_match_result(self,obj):
        return obj.score_display

