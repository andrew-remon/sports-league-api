# third-party
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

# local
from accounts.views import RegisterView, CustomTokenObtainPairView, ProfileView, LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
