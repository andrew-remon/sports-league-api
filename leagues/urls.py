from django.urls import path, include
from leagues.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'leagues', LeagueViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'matches', MatchViewSet)


urlpatterns = [
    # path('leagues/', league_collection_view, name="leagues-list"),
    # path('leagues/<int:league_id>/', retrieve_league_by_id, name="specific-league"),
    # path('leagues/<int:league_id>/teams/', team_collection_view, name="teams-list"),
    # path('v1/leagues/', LeagueListCreateAPIView.as_view(), name="v1_league_list"),
    path('v1/', include(router.urls))
]
