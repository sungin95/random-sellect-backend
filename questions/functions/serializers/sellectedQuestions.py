from questions.functions.serializers.serializers import (
    QuestionsSerializer,
    QuestionsCreateSerializer,
    SellectedQuestionSerializer,
    ShowSellectedQuestionSerializer,
    ImportanceSellectedQuestionSerializer,
)
from rest_framework.exceptions import ParseError
from questions.models import Questions, SellectedQuestions
from django.db import transaction


# get
def serializer_get_sellectedQuestion(questions):
    return ShowSellectedQuestionSerializer(questions)


def serializer_get_sellectedQuestions(questions):
    return ShowSellectedQuestionSerializer(questions, many=True)


# create
@transaction.atomic(using="default")
def serializer_create_sellectedQuestion(request, question: Questions):
    try:
        with transaction.atomic():
            sellectedQuestionSerializer = SellectedQuestionSerializer(
                data=QuestionsCreateSerializer(question).data,
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
    except:
        pass
    raise ParseError


# put
def serializer_put_sellectedQuestion_importance(
    request, sellectedQuestion: SellectedQuestions
):
    if request.data["importance"]:
        sellectedQuestion_importance_dict = {
            "importance": sellectedQuestion.importance
            + int(request.data["importance"]),
        }
        serializer = ImportanceSellectedQuestionSerializer(
            sellectedQuestion,
            data=sellectedQuestion_importance_dict,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return serializer
    return None
