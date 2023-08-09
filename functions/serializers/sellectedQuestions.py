from questions.serializers import (
    QuestionsCreateSerializer,
    SellectedQuestionSerializer,
    ShowSellectedQuestionSerializer,
    ImportanceSellectedQuestionSerializer,
)
from questions.models import Questions, SellectedQuestions


# get
def serializer_get_sellectedQuestion(questions):
    return ShowSellectedQuestionSerializer(questions)


def serializer_get_sellectedQuestions(questions):
    return ShowSellectedQuestionSerializer(questions, many=True)


# create
def serializer_create_sellectedQuestion(request, question: Questions):
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
            "data": sellectedQuestionSerializer.data,
            "model": sellectedQuestion,
        }
    return {"errors": sellectedQuestionSerializer}


# put
def serializer_put_sellectedQuestion_importance(
    importance, sellectedQuestion: SellectedQuestions
):
    sellectedQuestion_importance_dict = {
        "importance": sellectedQuestion.importance_calc(int(importance)),
    }
    serializer = ImportanceSellectedQuestionSerializer(
        sellectedQuestion,
        data=sellectedQuestion_importance_dict,
        partial=True,
    )
    if serializer.is_valid():
        serializer.save()
        return {"data": serializer.data}
    return {"errors": serializer.errors}
