from questions.functions.serializers.serializers import (
    QuestionsSerializer,
    QuestionsCreateSerializer,
    SellectedQuestionSerializer,
    ShowSellectedQuestionSerializer,
    ImportanceSellectedQuestionSerializer,
)
from rest_framework.exceptions import ParseError
from questions.models import Questions

# serializer 관리
# # get
# def serializer_sellectedQuestions_get(questions):
#     return QuestionsSerializer(questions, many=True)


# create
def serializer_create_sellectedQuestion(request, question):
    sellectedQuestionSerializer = SellectedQuestionSerializer(
        data=request.data,
    )
    if sellectedQuestionSerializer.is_valid():
        sellectedQuestion = sellectedQuestionSerializer.save(
            user=request.user,
            question=question,
        )
        # SQ 생성시 마다 해당 question 카운트 1을 올려준다.
        question.count_n(1)

        return {
            "serializer": sellectedQuestionSerializer,
            "model": sellectedQuestion,
        }
    raise ParseError
