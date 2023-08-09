from questions.serializers import (
    QuestionsSerializer,
    QuestionsCreateSerializer,
)


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
