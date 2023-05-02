from rest_framework.serializers import ModelSerializer
from .models import User


class UserCheckSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "username",
        )


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)
