from rest_framework.serializers import ModelSerializer
from .models import SellectedQuestion


class SellectedQuestionSerializer(ModelSerializer):
    class Meta:
        model = SellectedQuestion
        fields = ("description",)


class ShowSellectedQuestionSerializer(ModelSerializer):
    class Meta:
        model = SellectedQuestion
        fields = (
            "pk",
            "description",
            "importance",
        )


class ImportanceSellectedQuestionSerializer(ModelSerializer):
    class Meta:
        model = SellectedQuestion
        fields = ("importance",)
