from rest_framework.serializers import ModelSerializer
from .models import Questions, QuestionUser
from users.serializers import UserCheckSerializer


class QuestionsSerializer(ModelSerializer):
    authon = UserCheckSerializer(
        read_only=True,
    )

    class Meta:
        model = Questions
        fields = (
            "description",
            "authon",
        )


class QuestionsCreateSerializer(ModelSerializer):
    class Meta:
        model = Questions
        fields = ("description",)


class QuestionUserSerializer(ModelSerializer):
    class Meta:
        model = QuestionUser
        fields = ()
