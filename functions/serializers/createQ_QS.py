from .questions import serializer_create_questions
from .sellectedQuestions import serializer_create_sellectedQuestion
from django.db import transaction
from questions.models import Questions


@transaction.atomic(using="default")
def serializer_create_Question_sellectedQuestion(request):
    try:
        with transaction.atomic():
            questionSerializer = serializer_create_questions(request)
            if questionSerializer.get("errors") is not None:
                error = questionSerializer["errors"].errors
                raise
            sellectdQuestionSerializer = serializer_create_sellectedQuestion(
                request,
                questionSerializer["model"],
            )
            if sellectdQuestionSerializer.get("errors") is not None:
                error = questionSerializer["errors"].errors
                raise
            return {
                "question": questionSerializer["data"],
                "sellectdQuestion": sellectdQuestionSerializer["data"],
            }
    except:
        return {"errors": error}
