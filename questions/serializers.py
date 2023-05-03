from rest_framework.serializers import ModelSerializer
from .models import Questions
from users.serializers import UserCheckSerializer


class QuestionsSerializer(ModelSerializer):
    authon = UserCheckSerializer(
        read_only=True,
    )

    class Meta:
        model = Questions
        fields = (
            "pk",
            "description",
            "authon",
            "count",
        )


class QuestionsCreateSerializer(ModelSerializer):
    class Meta:
        model = Questions
        fields = ("description",)
