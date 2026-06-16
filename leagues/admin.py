from django.contrib import admin
from .models import League, Team, Player

# Register your models here.
@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_teams', 'created_at',)
    search_fields = ('name',)

    # todo: On Day 11, once I learn how QuerySets and annotations work, I will return to LeagueAdmin and replace max_teams or add a new column to show the active team count


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
