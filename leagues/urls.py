from django.urls import path
from . import views

urlpatterns = [
    path('leagues/', views.league_collection_view, name="leagues-list"),
    path('leagues/<int:league_id>/', views.retrieve_league_by_id, name="specific-league"),
    path('leagues/<int:league_id>/teams/', views.team_collection_view, name="teams-list")
]
