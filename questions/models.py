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
