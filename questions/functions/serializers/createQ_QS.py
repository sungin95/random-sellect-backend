from .questions import serializer_create_questions
from .sellectedQuestions import serializer_create_sellectedQuestion
from django.db import transaction
from questions.models import Questions


@transaction.atomic(using="default")
def serializer_create_Question_sellectedQuestion(request):
    try:
        with transaction.atomic():
            questionSerializer = serializer_create_questions(request)
            sellectdQuestionSerializer = serializer_create_sellectedQuestion(
                request,
                questionSerializer["model"],
            )
            return {
                "question": questionSerializer["serializer"],
                "ellectdQuestion": sellectdQuestionSerializer["serializer"],
            }
    except:
        return None
