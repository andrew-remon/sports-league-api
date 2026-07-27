# third-party
from rest_framework import serializers

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
