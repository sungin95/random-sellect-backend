from rest_framework.serializers import ModelSerializer
from .models import Questions
from users.serializers import UserCheckSerializer
from .models import SellectedQuestions


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
        fields = (
            "pk",
            "description",
        )


# ------------- SellectedQuestions ---------------


class SellectedQuestionSerializer(ModelSerializer):
    class Meta:
        model = SellectedQuestions
        fields = (
            "pk",
            "description",
        )


class ShowSellectedQuestionSerializer(ModelSerializer):
    class Meta:
        model = SellectedQuestions
        fields = (
            "pk",
            "description",
            "importance",
        )


class ImportanceSellectedQuestionSerializer(ModelSerializer):
    class Meta:
        model = SellectedQuestions
        fields = ("importance",)
