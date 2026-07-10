from django.contrib import admin, messages
from django.db.models import Count
from .models import *

# Register your models here.
class TeamInline(admin.TabularInline):
    model = Team
    extra = 1

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', "max_teams", 'created_at', 'get_team_count')
    search_fields = ('name',)
    inlines=[TeamInline]

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
    list_display = ('name', 'league', 'city', 'get_player_count', 'founded_year')
    list_select_related = ('league',)
    list_filter = ('league', 'city')
    search_fields = ('name', 'city', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(player_count=Count("players"))

    @admin.display(description="Player Count", ordering="player_count")
    def get_player_count(self, obj):
        return obj.player_count

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'team', 'position', 'jersey_number')
    list_select_related = ('team',)
    list_filter = ('position', 'team__league')
    search_fields = ('first_name', 'last_name',)

    @admin.display(description='Full Name', ordering='first_name')
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class MatchResultInline(admin.TabularInline):
    model = MatchResult
    extra = 0
    max_num = 1

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    inlines = [MatchResultInline]
    list_display = ('league', 'home_team', 'away_team', 'match_day', 'status', 'score_display')
    actions=["mark_matches_as_complete"]

    @admin.display(description="Match Result")
    def score_display(self,obj):
        return obj.score_display

    @admin.action(description="Mark selected matches as COMPLETED")
    def mark_matches_as_complete(self, request, queryset):
        matches_selected = queryset.update(status=Match.MatchStatus.COMPLETED)
        self.message_user(request, f"{matches_selected} Matches selected is marked as completed", messages.INFO)


