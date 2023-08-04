from django.db import models
from common.models import CommonModel
from users.models import User


class Question(CommonModel):
    description = models.TextField()

    class Meta:
        abstract = True


# 공용 질문
class Questions(Question):
    authon = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    count = models.PositiveIntegerField(default=1)

    def create_test_list(n: int, user: User):
        questions_list = []
        for i in range(n):
            questions_list.append(
                Questions.objects.create(
                    description="test description " + str(i),
                    authon=user,
                )
            )
        return questions_list


# 개인 질문 모음
class SellectedQuestions(Question):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    importance = models.PositiveIntegerField(default=3)
    question = models.ForeignKey(
        "Questions",
        on_delete=models.SET_NULL,
        null=True,
        related_name="questions_set",
    )

    def create_test(user: User, question_pk: Questions):
        question = Questions.objects.get(pk=question_pk)
        sellected_question = SellectedQuestions.objects.create(
            description=question.description,
            user=user,
            question=question,
        )
        return sellected_question
