# third-party
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

#local
from accounts.serializers import UserRegistrationSerializer

# Create your views here.
class RegisterView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

