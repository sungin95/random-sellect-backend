from django.db import models
from common.models import CommonModel


class SellectedQuestion(CommonModel):
    question = models.ForeignKey(
        "questions.Questions",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="questions",
    )
    description = models.TextField()
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    importance = models.PositiveIntegerField(default=3)

