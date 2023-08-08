from questions.serializers import (
    QuestionsSerializer,
    QuestionsCreateSerializer,
    SellectedQuestionSerializer,
    ShowSellectedQuestionSerializer,
    ImportanceSellectedQuestionSerializer,
)
from rest_framework.exceptions import ParseError


def serializer_get_questions(questions):
    return QuestionsSerializer(questions, many=True)


def serializer_create_questions(request):
    questionSerializer = QuestionsCreateSerializer(data=request.data)
    if questionSerializer.is_valid():
        question = questionSerializer.save(authon=request.user)
        return {
            "data": questionSerializer.data,
            "model": question,
        }
    return {"errors": questionSerializer}
