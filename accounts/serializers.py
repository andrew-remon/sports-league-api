# third-party
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# local
from accounts.models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializes User Registration for the public API."""

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type":"password"} # make password -> **** in browsable API.
        )

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "id",
        ]

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes user profile for public API."""

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "date_joined",
        ]
        read_only_fields = ["email", "date_joined",]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['first_name'] = user.first_name

        return token

    def validate(self, attrs):
        full_data = super().validate(attrs)

        user_data = {
            "user" : {
                "id": self.user.pk,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
            }
        }

        full_data.update(user_data)

        return full_data
