from .questions import serializer_create_questions
from .sellectedQuestions import serializer_create_sellectedQuestion
from django.db import transaction
from functions.functions import errors_check


@transaction.atomic(using="default")
def serializer_create_Question_sellectedQuestion(request):
    try:
        with transaction.atomic():
            questionSerializer = serializer_create_questions(request)
            if errors_check(questionSerializer):
                sellectdQuestionSerializer = serializer_create_sellectedQuestion(
                    request,
                    questionSerializer["model"],
                )
                if errors_check(sellectdQuestionSerializer):
                    return {
                        "question": questionSerializer["data"],
                        "sellectdQuestion": sellectdQuestionSerializer["data"],
                    }
                else:
                    error = sellectdQuestionSerializer["errors"].errors
                    raise
            else:
                error = questionSerializer["errors"].errors
                raise
    except:
        return {"errors": error}
