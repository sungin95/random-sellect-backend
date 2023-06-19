from django.db import models
from common.models import CommonModel


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
        blank=True,  # 나중에 삭제
        related_name="questions_set",
    )
