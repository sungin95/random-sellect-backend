from django.db import models
from common.models import CommonModel
from users.models import User
from rest_framework.exceptions import NotFound
from django.db import transaction
from rest_framework.exceptions import ParseError


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
    count = models.PositiveIntegerField(default=0)

    def get_object(pk: int):
        try:
            return Questions.objects.get(pk=pk)
        except Questions.DoesNotExist:
            raise NotFound

    def count_n(self, n: int):
        self.count += n
        self.save()

    def create_test_list(n: int, user: User) -> list:
        questions_list = []
        for i in range(n):
            question = Questions.objects.create(
                description="test description " + str(i),
                authon=user,
            )
            # 질문 만들면 나의 질문에도 자동 추가
            sellected_question = SellectedQuestions.create_test(
                user,
                question.pk,
            )
            questions_list.append((question, sellected_question))
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

    def get_object(pk: int) -> object:
        try:
            return SellectedQuestions.objects.get(pk=pk)
        except SellectedQuestions.DoesNotExist:
            raise NotFound

    @transaction.atomic(using="default")
    def create_test(user: User, question_pk: Questions):
        try:
            with transaction.atomic():
                question = Questions.objects.get(pk=question_pk)
                question.count += 1
                question.save()
                sellected_question = SellectedQuestions.objects.create(
                    description=question.description,
                    user=user,
                    question=question,
                )
                return sellected_question
        except:
            raise ParseError

    @transaction.atomic(using="default")
    def delete_count(self, question_pk: int):
        try:
            with transaction.atomic():
                question = Questions.get_object(question_pk)
                question.count_n(-1)
                self.delete()
        except:
            raise ParseError
