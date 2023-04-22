from rest_framework.serializers import ModelSerializer
from .models import SellectedQuestion


class SellectedQuestionSerializer(ModelSerializer):
    class Meta:
        model = SellectedQuestion
        fields = ()
