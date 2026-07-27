# third-party
from django.urls import path

# local
from accounts.views import RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register")
]
