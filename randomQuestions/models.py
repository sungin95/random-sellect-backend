from django.db import models
from common.models import CommonModel


class Questions(CommonModel):
    description = models.TextField()
    authon = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )

    def count(self):
        return self.questions.count()


class QuestionUser(CommonModel):
    question = models.ForeignKey(
        "Questions",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="questions",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    importance = models.PositiveIntegerField(default=3)
